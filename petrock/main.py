import logging


import guidance
from guidance import system, user, assistant, gen
from petrock.entities import Personality, Petrock
from petrock.vision import Vision
from petrock.llms import summon_llm

rp_system = "Roleplay according to the description, without breaking character for any reason whatsoever. Answer briefly and only in dialogue. "

# Test capacity.
class Echo:
    def echo(self):
        logging.debug(f"ECHO: {self.__class__.__name__.upper()}")


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
    logging.basicConfig(level=logging.INFO)
    llm = summon_llm("llama3", echo=False)

    for i in range(3):
        logging.info(f"Invoking Rocky to ask about its day, #{i}.")
        llm += invoke(rocky, "How's your day?")

        print(f"#{i+1}: {llm['latest_response'] + llm['stop']}")