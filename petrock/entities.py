from dataclasses import dataclass


@dataclass
class Personality:
    vibe: str
    purpose: str


class Entity:
    def __init__(self, capacities: list=None,
                 **kwargs):
        if capacities is None:
            return
        else:
            self.capacities = capacities
        # Allows capacities to be invoked by an entity.
        for capacity in self.capacities:
            setattr(self, capacity.__class__.__name__.lower(), capacity)


class Petrock(Entity):
    def __init__(self, persona: Personality, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.persona = persona

    @property
    def system(self):
        persona = self.persona
        out = [f"You are a {persona.vibe} pet rock. ",
                f"Your purpose for existing is {persona.purpose}."]
        return '\n'.join(out)