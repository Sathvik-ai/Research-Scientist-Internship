from faker import Faker
from random import uniform

fake = Faker()


def generate_task_name(project_type='engineering'):
    # Placeholder LLM-like variations using faker
    patterns = [
        '{component} - {action} - {detail}',
        '{action} {component}',
        '{component}: {goal}'
    ]
    component = fake.bs().split()[0].title()
    action = fake.word().capitalize()
    detail = fake.sentence(nb_words=3).rstrip('.')
    goal = fake.sentence(nb_words=4).rstrip('.')
    pattern = fake.random_element(elements=patterns)
    return pattern.format(component=component, action=action, detail=detail, goal=goal)


def generate_description(task_name='', project_context=''):
    # Simulate LLM output: varied length and optional acceptance criteria
    roll = uniform(0, 1)
    if roll < 0.2:
        return ''
    if roll < 0.6:
        return fake.sentence(nb_words=12)
    # longer with acceptance criteria
    bullets = '\n'.join(['- ' + fake.sentence(nb_words=6) for _ in range(2)])
    return f"{fake.paragraph(nb_sentences=2)}\n\nAcceptance criteria:\n{bullets}"
