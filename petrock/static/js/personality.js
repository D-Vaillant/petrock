const personas = {
    'cool': ['chill', 'wax philosophical about nonsense.'],
    'normal': ['boring', 'respond plainly and normally.'],
    'angry': ['irritable', 'be rude for no reason.']
};

function selectPersonality(personality) {
    const selectedPersonality = personas[personality];
    const vibe = selectedPersonality[0];
    const purpose = selectedPersonality[1];

    document.getElementById('personality').textContent = vibe;
    document.getElementById('purpose').textContent = purpose;

    const choices = document.querySelectorAll('.personality-choice');
    choices.forEach(choice => {
        if (choice.id === personality) {
            choice.classList.add('selected');
        } else {
            choice.classList.remove('selected');
        }
    });
}  