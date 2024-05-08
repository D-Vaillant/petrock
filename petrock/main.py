import guidance
from guidance import system, user, assistant, gen
from entities import Personality, Petrock
from vision import Vision, OpenCVWebcam
from llms import summon_llm

rp_system = "Roleplay according to the description, without breaking character for any reason whatsoever. Answer briefly and only in dialogue. "

# Test capacity.
class Echo:
    def echo(self):
        print(self.__class__.__name__.upper())


chill = Personality(vibe="relaxed", purpose="to be helpful and have a good time")
irascible = Personality(vibe="cranky", purpose="to stir up chaos")

sight = Vision()
rocky = Petrock(persona=irascible,
                capacities=[sight, Echo()])

@guidance
def invoke(llm, entity, prompt, **kwargs):
    sysprompt = kwargs.get("system_prompt", rp_system)
    with system():
        llm += sysprompt
        llm += entity.system
    with user():
        llm += prompt
    
    sentence_length = kwargs.get("sentence_length", 1)
    with assistant():
        for i in range(sentence_length):
            llm += gen(stop=['.', '!', '?'], name='latest_response',
                       save_stop_text='stop', temperature=0.7)

    return llm


if __name__ == "__main__":
    llm = summon_llm("llama3", echo=False)
    webcam = OpenCVWebcam()
    sight = Vision(device=webcam)
    rocky = Petrock(persona=irascible, capacities=[sight, Echo()])
    llm = summon_llm("llama3", echo=False)
    image = sight.use_webcam()
    caption = sight.caption_image(image)

    for i in range(5):
        llm += invoke(rocky, f"Caption: {caption}. How's your day?")

        print(f"#{i+1}: {llm['latest_response'] + llm['stop']}")