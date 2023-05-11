# LLaMA and Stable Diffusion Fine-Tuning Instructions

Rather than providing messy thrown together training code it is probably more useful to provide the original repositories which were used for fine tuning the models for this project. If trying to automate this project, I HIGHLY reccomend basing your work off the code in these existing repositories.

## Hardware

A Windows computer with a Ryzen 9 7950X, 32GB RAM, and RTX 3090 24GB GPU was used for training. Most importantly, make sure to have a GPU with 24GB of VRAM, having less VRAM may cause some training to fail, but it may be possible to use less with certain optimizations. Virtual environments were used for package installation. Windows Subsystem for Linux (WSL) was used sometimes, but it's probably reccomended.


## LLaMA Fine-Tuning Instructions

### Training Data

The training data for fine tuning the story generation model was generated with "chatgptstory.py". This generates the story/summary pairs by first asking ChatGPT for a summary, then to generate the story from the summary. Included is also a json file, train.json which is a json file with 1891 story summary pairs generated this way that was used for fine tuning.

### Fine Tuning

The fine-tuning was done using a very slightly modified version of https://github.com/lxe/simple-llm-finetuner

It is reccomended just to use the original simple-llm-finetuner repo, as it has been updated and is more up to date. The modifications we made are just in regards to how the training data is loaded in. 

For instance, we formatted the training messages in the following way: "You are a storyteller. Given a summary of a children's story, generate the full story. Make sure your story follows the same plot points of the summary and expands on each point. Make sure your story has a clear beginning, multiple plot points that build on each other, and a clear ending. \n Summary: \[story\] END \n Full story: \[story\] END"

The base model used was Facebook's LLaMA-7B model, available here. https://huggingface.co/decapoda-research/llama-7b-hf

Hugging Face's peft libary has been used with a LORA in order to improve training speed as reduce VRAM requirements. The instructions on the Github page are good, WSL was used. Note you MUST run "export LD_LIBRARY_PATH=/usr/lib/wsl/lib" for the GPU to used in WSL.

For the final model used, we trained on a ~80/20 training test split for 6 epochs, all other parameters were default.

The weights file for the LORA is small (only ~16MB) so I have included the weights in this repo for reference. (Just copy the folder lora-unsum-1536-6epoch). 

## Stable Diffusion Generation and Fine Tuning Instructions

Most of the image generated/fine-tuning with Dreambooth was done with https://github.com/AUTOMATIC1111/stable-diffusion-webui

See more details about Dreambooth here - https://dreambooth.github.io/

It is reccomended to download the latest version from Github. The Automatic1111 Web UI supports extensions, go to the "Extensions" Tab. The following extensions were used

* https://github.com/d8ahazard/sd_dreambooth_extension.git\
Used for fine tuning with Dreambooth
* https://github.com/AlUlkesh/stable-diffusion-webui-images-browser.git\
Image browser, used for easily searching through previously generated images
* https://github.com/Mikubill/sd-webui-controlnet.git\
ControlNet, used to generate images in certain poses

### Training Data

Dreambooth allows us to add particular subjects into a model via fine tuning. Each subject has an identifier and a class name, and should be prompted as such when generating images. (For instance, if I want to generate a specific cat with class name george then I would ask stable diffusion for a "george cat")

When picking identifier names to use, it is ideal to pick an identifier that is not commonly used on other context, "e.g. tom cat" would be a bad identifier choice, and is a single token. For instance, "ohwx" is a commonly chosen indentifier for that reason.

Training data for the cat and the dog was obtained from Instagram, and manually captioned. They are included here. There are roughly 20-30 images of each. 

Regularization images are also included. These are generic pictures of cats and dogs, generated via Stable Diffusion. The purpose of regularization images is to prevent overfitting, so that not all dogs for instance look like out fine tuned dog.

### Fine Tuning Settings

With the Dreambooth extension, first create a model based on the base StableDiffusion1.5 checkpoint. Then for each concept, e.g. a cat or a dog, set the dataset directory to the directory containing the training images/labels, and the classification directory to the directory containing regularization images. For the instance token, set it to your instnace token, and for the class token, set it to your class name. (e.g. ohwx and dog) For the instance prompt, set it to "\[filewords\]" and for the class prompt, set it to "photograph of \[class name\]". Set the sample image prompt to "photograph of \[instance name\] \[class name\]"

For training settings, generally the settings generated with Performance Wizard should be fine, but I trained for 100 epochs, batch size 4, 2 gradient accumulation steps, 8 bit Adam, fp16, and 0.75 prior loss weight, rest of parameters are default, on RTX 3090. Since the fine-tuned model is too large (~5GB) it is not provided in this repository.

### Image Generation

Once the model was properly trained, we can generate image with the txt2img tab. For generating images, I used DPM++ 2M Karras sampler, with 30 sampling steps. Batch size can be increased to generate more images in each run.

#### Prompting

Prompting is very much an art form with trial and error, and these is much to read about it online. Generally lists of subjects/backgrounds work best, along with specifying the art style. Negative prompts are also used.

For instance, when generating a picture of a cat, the following positive prompt was used "artistic digital painting of ((bhna cat)) (playing with ball of yarn), living room, house, fireplace, cozy lighting, 4k, 8k, global illumination, (highly detailed), (intricate), digital art featured on artstation", with negative prompt "blurry, ugly, ugly face, fat, low resolution, malformed, disfigured, deformed, photograph, canon f/1.6"

Note the use of parenthesis. Parenthesis can put extra emphasis on a particular term. "bhna" here is our fine tuned Dreambooth identifier. You can play around and see how keywords like global illumination and intricate affect image quality. Also note for instance, use of negative prompts like "canon f/1.6". This keyword is commonly associated with photographs, so that negative keyword will make the illustration less photorealistic.

#### Super-Resolution!

To increase image quality, we want to increase the resolution, as the default 512x512 the model outputs oftentimes lacks details. We are able to generate higher resolution images with Stable Diffusion (e.g. 1024x1024) but the issue is this is slower and more importantly there is often issues with aliasing and objects being copied/deformed. This is due to the fact that the model is trained on 512x512 images. However, to alievate this, first I generate many images with the 512x512 model. Then, when I find an image that looks good, I will send it to img2img. Then I enable ControlNet, using HED maps. Note that you will have to download the ControlNet model from here - https://huggingface.co/webui/ControlNet-modules-safetensors/tree/main

When using ControlNet, use the SAME image that you are doing img2img with. Then set the resolution to 1024x1024. This prevents aliasing as the ControlNet model "freezes" the form of the original image. In practice, you will end up with a 1024x1024 image that looks roughly the same as your original.

Then, in the extensions tab, this image is further upscaled to 4096x4096 using the 4x upscale with R-ESRGAN. https://github.com/xinntao/Real-ESRGAN









