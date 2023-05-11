import openai
openai.api_key = "sk-XXX"  # supply your API key however you choose

print(openai.Model.list())
import time

#completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a storyteller, who specializes in telling children's stories, using simple vocabulary. Your stories should be witty and lighthearted, with a clear instroduction, multiple plot points, and clear conclusion. You avoid writing very short stories, and your stories always have multiple paragraphs"}, {"role":"user", "content":"Tell me the story of Bob the pig"}])
start = 0
with open('summaries.txt', 'r') as f:
    l = f.readlines()
    start = int(l[-1].split("*")[0])
print(start)  #finds last entry in summaries, appends to the end

my_model = 'gpt-3.5-turbo'
my_model = 'gpt-4'


for i in range(start+1,10000):
    try:

        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "Your job as an assistant is to generate messages in the format the user specifies. You must follow the user's requested format, however you should also be as creative as possible in your responses while being concise. Your responses must have proper grammar and make sense. You do not always have to include optional parameters. You must respond with only the requested message and no introduction."}, {"role":"user", "content":"Please generate a message of the following format: [1] [2] [3] [4] [5] [6] [7] [8] \n In your response, you should replace each of the bracketed numbers with the appropriate phrase as follows - [1] is a unique name, [2] is an interesting character which may be a unique animal, or a person who may be male or female with a specific job or hobby, [3] is a short description of the character's appearance, interests, or personality, including particular positive or negative attributes of the character, [4] repesents one particular action or event this character does, or happens to this character. This action or event may or may not include other characters. [5] repesents another particular action or event this character does, or happens to this character. This action or event may or may not include other characters. [6] repesents another particular action or event this character does, or happens to this character. This action or event may or may not include other characters. [7] repesents another particular action or event this character does, or happens to this character. This action or event may or may not include other characters. [8] represents a conclusion to the story. Please ensure your response does not include [] characters. Be consise." }])
        story_plan = completion.choices[0].message.content


        print(story_plan)

        time.sleep(3)
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "You are a storyteller, who specializes in telling children's stories, using simple vocabulary. Your stories should be witty and lighthearted, with a clear instroduction, multiple continuous plot points that build on each other, and clear conclusion. Your stories should be at least 1000 words, and your stories always have multiple paragraphs. Your response should include nothing but the story"}, {"role":"user", "content":f"As a skilled storyteller, please tell a detailed version of thhe following story summary, expanding and adding plot detail to each plot point described in the following summary: {story_plan}"}])

        story = completion.choices[0].message.content

        time.sleep(3)

        print(story)

        with open('summaries.txt', 'a') as f:
            a= story_plan.replace('\n', ' ')
            f.write(f"{i} * {a} "+"\n")

        with open('stories.txt', 'a') as f:
            a = story.replace('\n', ' ')
            f.write(f"{i} * {a} "+"\n")
    except:
        i-=1
        aaa+=1
        print('oops')
        time.sleep(60)
    