import os
import pickle
import numpy as np
from music21 import converter, instrument, note, chord
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from keras.utils import to_categorical
import tensorflow as tf

def parse_midi_files(data_dir):
    notes = []
    for file in os.listdir(data_dir):
        if file.endswith(".mid"):
            midi = converter.parse(os.path.join(data_dir, file))
            notes_to_parse = None
            parts = instrument.partitionByInstrument(midi)
            if parts:  # file has instrument parts
                notes_to_parse = parts.parts[0].recurse()
            else:  # file has notes in a flat structure
                notes_to_parse = midi.flat.notes
            for element in notes_to_parse:
                if isinstance(element, note.Note):
                    notes.append(str(element.pitch))
                elif isinstance(element, chord.Chord):
                    notes.append('.'.join(str(n) for n in element.normalOrder))
    return notes

def prepare_sequences(notes, n_vocab):
    sequence_length = 100
    note_to_int = dict((note, number) for number, note in enumerate(sorted(set(notes))))
    network_input = []
    network_output = []
    for i in range(0, len(notes) - sequence_length):
        sequence_in = notes[i:i + sequence_length]
        sequence_out = notes[i + sequence_length]
        network_input.append([note_to_int[char] for char in sequence_in])
        network_output.append(note_to_int[sequence_out])
    n_patterns = len(network_input)
    network_input = np.reshape(network_input, (n_patterns, sequence_length, 1))
    network_input = network_input / float(n_vocab)
    network_output = to_categorical(network_output)
    return network_input, network_output, note_to_int

def create_model(network_input, n_vocab):
    model = Sequential()
    model.add(LSTM(256, input_shape=(network_input.shape[1], network_input.shape[2]), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(256))
    model.add(Dropout(0.2))
    model.add(Dense(n_vocab, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

def main():
    # Enable GPU acceleration
    physical_devices = tf.config.list_physical_devices('GPU')
    if physical_devices:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    notes = parse_midi_files('data')
    n_vocab = len(set(notes))
    network_input, network_output, note_to_int = prepare_sequences(notes, n_vocab)
    
    # Save preprocessed data
    with open('preprocessed_data.pkl', 'wb') as f:
        pickle.dump({
            'note_to_int': note_to_int,
            'network_input': network_input,
            'n_vocab': n_vocab
        }, f)
    
    model = create_model(network_input, n_vocab)
    filepath = "models/melodia-{epoch:02d}-{loss:.4f}.keras"
    checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=0, save_best_only=True, mode='min')
    early_stopping = EarlyStopping(monitor='loss', patience=10, verbose=1)
    reduce_lr = ReduceLROnPlateau(monitor='loss', factor=0.2, patience=5, min_lr=0.001, verbose=1)
    
    model.fit(network_input, network_output, epochs=200, batch_size=64, callbacks=[checkpoint, early_stopping, reduce_lr])
    
    # Save the final model
    model.save('models/melodia_final_model.keras')

if __name__ == '__main__':
    main()