import graphviz

# Re-create a Digraph object for the new DFA after the reset
dfa_c = graphviz.Digraph()

# Define the DFA states and transitions
dfa_c.attr(rankdir='LR', size='8,5')

# Define DFA states
dfa_c.attr('node', shape='circle')
dfa_c.node('q0', 'q0')
dfa_c.node('q1', 'q1')
dfa_c.node('q2', 'q2')
dfa_c.node('q3', 'q3')
dfa_c.attr('node', shape='doublecircle')  # Accepting state
dfa_c.node('q4', 'q4')

# Define DFA transitions for 'a' and 'b'
dfa_c.edge('q0', 'q1', 'a')
dfa_c.edge('q1', 'q2', 'a')
dfa_c.edge('q2', 'q2', 'a')
dfa_c.edge('q2', 'q2', 'b')
dfa_c.edge('q2', 'q3', 'b')
dfa_c.edge('q3', 'q4', 'b')

# Define non-accepting transitions for 'b' at the start and 'a' after q3
dfa_c.attr('node', shape='circle', style='filled', color='lightgrey')
dfa_c.node('qa', 'qa')  # dead state for 'b' at the start
dfa_c.node('qb', 'qb')  # dead state for 'a' after q3
dfa_c.edge('q0', 'qa', 'b')
dfa_c.edge('q1', 'qa', 'b')
dfa_c.edge('q3', 'qb', 'a')
dfa_c.edge('qa', 'qa', 'a')
dfa_c.edge('qa', 'qa', 'b')
dfa_c.edge('qb', 'qb', 'a')
dfa_c.edge('qb', 'qb', 'b')

# The graph is saved as a PNG file
file_path_c = './mnt/data/dfa_c.png'
dfa_c.render(file_path_c, view=False, format='png')


