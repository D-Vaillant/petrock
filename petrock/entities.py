from dataclasses import dataclass
import logging

import guidance
from guidance import system, user, assistant, gen

@dataclass
class Personality:
    vibe: str
    purpose: str


rp_system = "Roleplay according to the description, without breaking character for any reason whatsoever. Answer briefly and only in dialogue. "


class Entity:
    def __init__(self, capacities: list=None,
                 **kwargs):
        if capacities is None:
            return
        else:
            self.capacities = capacities
        # Allows capacities to be utilized by an entity.
        # e.g. e = Entity(capacities=[Vision(), Dance()])
        # e.vision.do_vision(); e.dance.do_dance();
        for capacity in self.capacities:
            setattr(self, capacity.__class__.__name__.lower(), capacity)

    @property
    def system(self):
        # Overwrite this for your Entity subclasses.
        return ''

    @guidance
    def chat(llm, self, prompt):
        with system():
            llm += rp_system
            llm += self.system
        with user():
            llm += prompt
        with assistant():
            llm += gen(max_tokens=500, name='response')
        logging.info("Entity Response: {llm['response']}")
        return llm


class Petrock(Entity):
    def __init__(self, persona: Personality|tuple, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(persona, tuple):
            persona = Personality(*persona)
        self.persona = persona

    @property
    def system(self):
        persona = self.persona
        out = [f"You are a {persona.vibe} pet rock. ",
                f"Your purpose for existing is {persona.purpose}."]
        return '\n'.join(out)