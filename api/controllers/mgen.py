import base64
from io import BytesIO
import os
import time
import random
from datetime import datetime
from typing import List, Dict
from midiutil import MIDIFile
from api.db.connection import Database
from algorithms.genetic import generate_genome, Genome, selection_pair, single_point_crossover, mutation
client = Database().getConnection()
musicComposerDB = client.musicComposerCollection
musicComposerDBFiles = musicComposerDB.files
BITS_PER_NOTE = 4
KEYS = ["C", "C#", "Db", "D", "D#", "Eb", "E", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B"]
SCALES = ["major", "minorM", "dorian", "phrygian", "lydian", "mixolydian", "majorBlues", "minorBlues"]


class MgenController():

    def int_from_bits(self, bits: List[int]) -> int:
        return int(sum([bit * pow(2, index) for index, bit in enumerate(bits)]))

    def genome_to_melody(self, genome: Genome, num_bars: int, num_notes: int, num_steps: int,
                        pauses: int, key: str, scale: str, root: int) -> Dict[str, list]:
        notes = [genome[i * BITS_PER_NOTE:i * BITS_PER_NOTE + BITS_PER_NOTE] for i in range(num_bars * num_notes)]

        note_length = 4 / float(num_notes)

        # Replace Pyo-related code with MIDI generation logic here
        melody = {
            "notes": [random.randint(0, 127) for _ in range(num_bars * num_notes)],
            "velocity": [127 for _ in range(num_bars * num_notes)],
            "beat": [note_length for _ in range(num_bars * num_notes)],
        }

        steps = []
        for step in range(num_steps):
            steps.append([note for note in melody["notes"]])

        melody["notes"] = steps
        return melody

    def fitness(self, genome: Genome, num_bars: int, num_notes: int, num_steps: int,
                pauses: bool, key: str, scale: str, root: int, bpm: int) -> int:
        # Replace Pyo-related code with fitness evaluation here
        rating = 4  # Assign a fixed value for 'rating'
        return rating

    def save_genome_to_midi(self, filename: str, genome: Genome, num_bars: int, num_notes: int, num_steps: int,
                            pauses: bool, key: str, scale: str, root: int, bpm: int):
        melody = self.genome_to_melody(genome, num_bars, num_notes, num_steps, pauses, key, scale, root)

        if len(melody["notes"][0]) != len(melody["beat"]) or len(melody["notes"][0]) != len(melody["velocity"]):
            raise ValueError

        mf = MIDIFile(1)

        track = 0
        channel = 0

        time = 0.0
        mf.addTrackName(track, time, "Sample Track")
        mf.addTempo(track, time, bpm)

        for i, vel in enumerate(melody["velocity"]):
            if vel > 0:
                for step in melody["notes"]:
                    mf.addNote(track, channel, step[i], time, melody["beat"][i], vel)

            time += melody["beat"][i]

        # Convert the MIDI data to bytes
        midi_buffer = BytesIO()
        mf.writeFile(midi_buffer)
        midi_data = midi_buffer.getvalue()
        midi_buffer.close()

        # Encode binary data in Base64
        midi_data_base64 = base64.b64encode(midi_data).decode('utf-8')

        # Save the bytes to the MongoDB database
        musicComposerDBFiles.insert_one({"filename": filename, "midi_data": midi_data_base64})

    def main(self, num_bars=8, num_notes=4, num_steps=1, pauses=True, key="C", scale="major", root=4,
             population_size=10, num_mutations=2, mutation_probability=0.5, bpm=128):

        folder = f"{str(int(datetime.now().timestamp()))}"

        os.makedirs(folder, exist_ok=True)

        population = [generate_genome(num_bars * num_notes * BITS_PER_NOTE) for _ in range(population_size)]

        population_id = 0

        running = True
        while running:
            random.shuffle(population)

            population_fitness = [(genome, self.fitness(genome, num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)) for genome in population]

            sorted_population_fitness = sorted(population_fitness, key=lambda e: e[1], reverse=True)

            population = [e[0] for e in sorted_population_fitness]

            next_generation = population[0:2]

            for j in range(int(len(population) / 2) - 1):

                def fitness_lookup(genome):
                    for e in population_fitness:
                        if e[0] == genome:
                            return e[1]
                    return 0

                parents = selection_pair(population, fitness_lookup)
                offspring_a, offspring_b = single_point_crossover(parents[0], parents[1])
                offspring_a = mutation(offspring_a, num=num_mutations, probability=mutation_probability)
                offspring_b = mutation(offspring_b, num=num_mutations, probability=mutation_probability)
                next_generation += [offspring_a, offspring_b]

            print(f"population {population_id} done")

            for i, genome in enumerate(population):
                filename = f"{folder}/{scale}-{key}-{i}.mid"
                self.save_genome_to_midi(filename, genome, num_bars, num_notes, num_steps, pauses, key, scale, root, bpm)

            print(f"Saved to folder: {folder}")

            running = False
            population = next_generation
            population_id += 1


