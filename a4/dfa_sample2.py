# DFA Minimization using the table filling algorithm to merge equivalent states
def minimize_dfa_states(dfa_config):
    non_final_states = set(dfa_config['states']) - dfa_config['accept_states']
    final_states = dfa_config['accept_states']
    state_transitions = dfa_config['transitions']
    
    # Initialize the table
    distinguishable_pairs = set()
    for state1 in non_final_states:
        for state2 in final_states:
            distinguishable_pairs.add((state1, state2))
    
    # Mark distinguishable states
    is_changed = True
    while is_changed:
        is_changed = False
        for state1 in dfa_config['states']:
            for state2 in dfa_config['states']:
                if state1 < state2 and (state1, state2) not in distinguishable_pairs:
                    for input_char in dfa_config['alphabet']:
                        next_state1 = state_transitions.get((state1, input_char))
                        next_state2 = state_transitions.get((state2, input_char))
                        if (next_state1, next_state2) in distinguishable_pairs or (next_state2, next_state1) in distinguishable_pairs:
                            distinguishable_pairs.add((state1, state2))
                            is_changed = True
                            break

    # Merge equivalent states
    equivalent_states = {}
    for state1 in dfa_config['states']:
        for state2 in dfa_config['states']:
            if state1 < state2 and (state1, state2) not in distinguishable_pairs:
                if state1 not in equivalent_states:
                    equivalent_states[state1] = f"{state1}/{state2}"
                equivalent_states[state2] = equivalent_states[state1]
    
    merged_states = set(equivalent_states.values())
    minimized_dfa = {
        'states': list(merged_states),
        'alphabet': dfa_config['alphabet'],
        'transitions': {},
        'start_state': equivalent_states.get(dfa_config['start_state'], dfa_config['start_state']),
        'accept_states': set([equivalent_states.get(state, state) for state in final_states])
    }
    
    for (origin_state, input_char), destination_state in state_transitions.items():
        origin_state_merged = equivalent_states.get(origin_state, origin_state)
        destination_state_merged = equivalent_states.get(destination_state, destination_state)
        minimized_dfa['transitions'][(origin_state_merged, input_char)] = destination_state_merged
    
    return minimized_dfa

# DFA Simulator for computation on input string
def run_dfa_simulation(dfa_config, input_str):
    current_state = dfa_config['start_state']
    step = 0
    
    for char in input_str:
        next_state = dfa_config['transitions'].get((current_state, char))
        remaining_str = input_str[step + 1:]
        remaining_str_display = remaining_str if remaining_str else 'λ'
        
        if next_state is None:
            return f"Computation: Reject"
        current_state = next_state
        step += 1
    
    return f"Computation: {'Accept' if current_state in dfa_config['accept_states'] else 'Reject'}"

def read_dfa_from_file(filepath):
    dfa_config = {
        'states': set(),
        'alphabet': set(),
        'transitions': {},
        'start_state': '',
        'accept_states': set()
    }

    with open(filepath, 'r') as file:
        for line in file:
            line = line.strip()  # Remove trailing newline character
            if not line:
                continue  # Skip empty lines

            if '-->' in line:
                # This is the start state
                start_state = line.split('-->')[1].strip()
                dfa_config['start_state'] = start_state
                dfa_config['states'].add(start_state)
            elif '*' in line:
                # This is an accepting state
                accept_state = line.split('*')[1].strip()
                dfa_config['accept_states'].add(accept_state)
                dfa_config['states'].add(accept_state)
            else:
                # This is a transition
                state, transitions = line.split(':')
                state = state.strip()
                dfa_config['states'].add(state)
                for transition in transitions.split(','):
                    input_symbol, next_state = transition.split('->')
                    input_symbol = input_symbol.strip()
                    next_state = next_state.strip()
                    dfa_config['alphabet'].add(input_symbol)
                    dfa_config['transitions'][(state, input_symbol)] = next_state

    return dfa_config


filepaths = ['dfa1.txt', 'dfa2.txt']
for filepath in filepaths:
    dfa = read_dfa_from_file(filepath)
    
    input_string = input(f'Enter computation string for {filepath}: ')
    print('Computation result:', run_dfa_simulation(dfa, input_string))
    
    # Minimize the DFA
    minimized_dfa = minimize_dfa_states(dfa)
    
    # Simulate the minimized DFA on the given string
    result = run_dfa_simulation(minimized_dfa, input_string)
    print("Minimized DFA:", minimized_dfa)
    print("Simulation Result:", result)

