from __future__ import print_function
import re
import spacy
import random
from pyclausie import ClausIE

nlp = spacy.load('en')
re_spaces = re.compile(r'\s+')
persons = []
pets = []
trips = []


class Person(object):
    def __init__(self, name, likes=None, has=None, travels=None):
        """
        :param name: the person's name
        :type name: basestring
        :param likes: (Optional) an initial list of likes
        :type likes: list
        :param dislikes: (Optional) an initial list of likes
        :type dislikes: list
        :param has: (Optional) an initial list of things the person has
        :type has: list
        :param travels: (Optional) an initial list of the person's travels
        :type travels: list
        """
        self.name = name
        self.likes = [] if likes is None else likes
        self.has = [] if has is None else has
        self.travels = [] if travels is None else travels

    def __repr__(self):
        return self.name


class Pet(object):
    def __init__(self, pet_type, name=None):
        self.name = name
        self.type = pet_type


class Trip(object):
    def __init__(self, departs_on=None, departs_to=None, departs_time=None):
        self.departs_on = departs_on
        self.departs_to = departs_to
        self.departs_time = departs_time


def get_data_from_file(file_path='./test.txt'):
    with open(file_path) as infile:
        cleaned_lines = [line.strip() for line in infile if
                         (not line.startswith(('$$$', '###', '===', '/n'))) and line != '']

    return cleaned_lines


def select_person(name):
    for person in persons:
        if person.name == name:
            return person


def add_person(name):
    person = select_person(name)

    if person is None:
        new_person = Person(name)
        persons.append(new_person)

        return new_person

    return person


def select_pet(name):
    for pet in pets:
        if pet.name == name:
            return pet


def add_pet(type, name=None):
    pet = None

    if name:
        pet = select_pet(name)

    if pet is None:
        pet = Pet(type, name)
        pets.append(pet)

    return pet

def select_trip(time,name):
    # type: (object, object) -> object
    for trip in trips:
        if trip.name==name and trip.time==time:
            return trip

def add_trip(time, name, destination_to=None):
    trip = select_trip(time,name)

    if trip is None:
        new_trip=Trip(time, name, destination_to)
        trips.append(new_trip)

        return new_trip

    return trip

def get_persons_pet(person_name):
    person = select_person(person_name)

    for thing in person.has:
        if isinstance(thing, Pet):
            return thing


# noinspection PyGlobalUndefined
def process_relation_triplet(triplet):
    """
    Process a relation triplet found by ClausIE and store the data
    find relations of types:
    (PERSON, likes, PERSON)
    (PERSON, has, PET)
    (PET, has_name, NAME)
    (PERSON, travels, TRIP)
    (TRIP, departs_on, DATE)
    (TRIP, departs_to, PLACE)
    :param triplet: The relation triplet from ClausIE
    :type triplet: tuple
    :return: a triplet in the formats specified above
    :rtype: tuple
    """

    sentence = triplet.subject + ' ' + triplet.predicate + ' ' + triplet.object

    doc = nlp(unicode(sentence))
    global root
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t

        # elif t.pos_ == 'NOUN'

    # also, if only one sentence
    # root = doc[:].root

    """
    CURRENT ASSUMPTIONS:
    - People's names are unique (i.e. there only exists one person with a certain name).
    - Pet's names are unique
    - The only pets are dogs and cats
    - Only one person can own a specific pet
    - A person can own only one pet
    """

    # Process (PERSON, likes, PERSON) relations
    if root.lemma_ == 'like':
        if triplet.subject in [e.text for e in doc.ents if e.label_ in ['PERSON', 'ORG']] and triplet.object in [e.text
                                                                                                                 for e
                                                                                                                 in
                                                                                                                 doc.ents
                                                                                                                 if
                                                                                                                 e.label_ in [
                                                                                                                     'PERSON']]:
            s = add_person(triplet.subject)
            o = add_person(triplet.object)
            s.likes.append(o)

    # Process (PET, has, NAME)
    if triplet.subject.endswith('name') and ('dog' in triplet.subject or 'cat' in triplet.subject):
        obj_span = doc.char_span(sentence.find(triplet.object), len(sentence))

        # handle single names, but what about compound names? Noun chunks might help.
        if len(obj_span) == 1 and obj_span[0].pos_ == 'PROPN':
            name = triplet.object
            subj_start = sentence.find(triplet.subject)
            subj_doc = doc.char_span(subj_start, subj_start + len(triplet.subject))

            s_people = [token.text for token in subj_doc if token.pos_ == 'PROPN']
            s_person = add_person(s_people[0])

            s_pet_type = 'dog' if 'dog' in triplet.subject else 'cat'

            pet = add_pet(s_pet_type, name)

            s_person.has.append(pet)

    if root.lemma_ == 'have' and ('dog' in triplet.object or 'cat' in triplet.object) and 'named' in triplet.object:
        s = add_person(triplet.subject)
        named_doc = nlp(unicode(triplet.object))
        name_t = [t for t in named_doc if t.text == 'named'][0]
        name_what = [t for t in name_t.children][0].text
        s_pet_type = 'dog' if 'dog' in triplet.object else 'cat'
        pet = add_pet(s_pet_type, name_what)
        s.has.append(pet)
    # Process (PERSON, likes, PERSON) relations
    if 'like' == root.lemma_ and 'does' not in triplet.predicate and triplet.subject in [e.text for e in doc.ents if
                                                                                         e.label_ == 'PERSON' or (
                                                                                                 e.label_ == 'ORG')] and triplet.object in [
        e.text for e in
        doc.ents if
        e.label_ == 'PERSON' or (
                e.label_ == 'ORG')]:
        s = add_person(triplet.subject)
        o = add_person(triplet.object)
        s.likes.append(o)
    if root.lemma_ == 'be' and triplet.object.startswith('friends with'):
        fw_doc = nlp(unicode(triplet.object))
        with_token = [t for t in fw_doc if t.text == 'with'][0]
        fw_who = [t for t in with_token.children if t.dep_ == 'pobj'][0].text

        if triplet.subject in [e.text for e in doc.ents if e.label_ == 'PERSON'] and fw_who in [e.text for e in doc.ents
                                                                                                if
                                                                                                e.label_ == 'PERSON']:
            s = add_person(triplet.subject)
            o = add_person(fw_who)
            s.likes.append(o)
            o.likes.append(s)


def preprocess_question(question):
    # remove articles: a, an, the

    q_words = question.split(' ')

    # when won't this work?
    for article in ('a', 'an', 'the'):
        try:
            q_words.remove(article)
        except:
            pass

    return re.sub(re_spaces, ' ', ' '.join(q_words))


def has_question_word(string):
    # note: there are other question words
    for qword in ('who', 'what', 'how', 'where'):
        if qword in string.lower():
            return True

    return False


def answer_question(question):
    cl = ClausIE.get_instance()
    q_trip = cl.extract_triples([preprocess_question(question)])[0]
    sentence1 = q_trip.subject + ' ' + q_trip.predicate + ' ' + q_trip.object
    doc = nlp(unicode(sentence1))
    raw = nlp(unicode(sentence1))
    for t in doc:
        if t.pos_ == 'VERB' and t.head == t:
            root = t
    # Who has a dog/cat
    if q_trip.subject.lower() == 'who' and (q_trip.object == 'dog'):
        answer = '{} has a {} named {}.'

        for person in persons:
            pet = get_persons_pet(person.name)
            if pet and pet.type == 'dog':
                print(answer.format(person.name, 'dog', pet.name))
    elif q_trip.subject.lower() == 'who' and q_trip.object == 'cat':
        answer = '{} has a {} named {}'

        for person in persons:
            pet = get_persons_pet(person.name)
            if pet and pet.type == 'cat':
                print(answer.format(person.name, 'cat', pet.name))

    # Who likes person Q 3>
    elif 'who' in q_trip.subject.lower() and root.lemma_ == 'like':
        qdoc = nlp(unicode(question))
        personB = [e.text for e in qdoc.ents if e.label_ == 'PERSON'][0]
        for person in persons:
            personlike = set(person.likes)
            for personC in personlike:
                if personC.name == personB:
                    print(person)

    # Does person like person?

    elif 'does' in q_trip.subject.lower() and 'like' in sentence1:
        list = [e.text for e in doc.ents if e.label_ == 'PERSON']
        person_sub = list[0]
        person_obj = list[1]
        x = 0
        for person in persons:
            if person.name == person_sub:
                for person1 in person.likes:
                    if person1.name == person_obj:
                        # print(x)

                        x = 1
        #                 print(x)
        # print(x)
        if x:
            print("Yes.")
        else:
            print("No")

    # What's the name of <person>'s <pet_type>?
    elif 'what' in [t.text.lower() for t in raw if t.dep_ == 'attr'] and (
            'dog' or 'cat' in [t.text.lower() for t in raw if t.dep_ == 'pobj']):
        name_p = str([t.text for t in doc.ents if (t.label_ == 'PERSON' or t.label_ == 'ORG')][0])
        if "dog" in [t.text.lower() for t in raw if t.dep_ == 'pobj']:
            pet_type = 'dog'
        else:
            pet_type = 'cat'
        pet_type2 = get_persons_pet(persons.name)
        for person in persons:
            if name_p == person.name:
                if pet_type2.type == pet_type:
                    print(name_p + ' has a ' + pet_type + ' named ' + pet_type2.name)
        else:
            print(name_p + ' has no ' + pet_type)
    elif q_trip.subject.lower() == 'who' and 'GPE' in [e.label_ for e in doc.ents]:
            answer = '{} is traveling to {}'
            print()
            check = 0
            travel_d = str([t.text for t in doc.ents if t.label_ == "GPE"][0])
            for person in persons:
                if travel_d in [trip.departs_to for trip in person.travels]:
                    print(answer.format(person.name, travel_d))
                    check = 1
            if check == 0:
                print(answer.format('Nobody', travel_d))
    else:
        print (" Sorry I dont have the answer for this question at the moment, but I am still learning.")

def main():
    sents = get_data_from_file()
    cl = ClausIE.get_instance()
    triples = cl.extract_triples(sents)

    for t in triples:
        r = process_relation_triplet(t)

    question = ' '
    while question[-1] != '?':
        question = raw_input("Please enter your question: ")

        if question[-1] != '?':
            print('This is not a question... please try again')

    q_trip = cl.extract_triples([preprocess_question(question)])[0]
    sentence1 = q_trip.subject + ' ' + q_trip.predicate + ' ' + q_trip.object
    # doc = nlp(unicode(sentence1))

    # (WHO, has, PET)
    # here's one just for dogs
    answer_question(question)


if __name__ == '__main__':
    main()
