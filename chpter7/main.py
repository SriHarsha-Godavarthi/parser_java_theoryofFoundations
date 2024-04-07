# from graphviz import Digraph

# # Function to create a PDA graph for the given language part
# def create_pda(part):
#     f = Digraph('finite_state_machine', filename=f'pda_{part}.gv')
#     f.attr(rankdir='LR', size='8,5')

#     f.attr('node', shape='point')
#     f.node('qi')  # Initial state

#     f.attr('node', shape='doublecircle')
#     f.node('q_accept')  # Accept state

#     f.attr('node', shape='circle')
#     if part == 'b':
#         # PDA for the language {a^i c^j b^i | i, j ≥ 0}
#         f.edge('qi', 'q0', label='ε,ε->Z')
#         f.edge('q0', 'q0', label='a,ε->a')
#         f.edge('q0', 'q1', label='c,ε->ε')
#         f.edge('q1', 'q1', label='c,ε->ε')
#         f.edge('q1', 'q2', label='b,a->ε')
#         f.edge('q2', 'q2', label='b,a->ε')
#         f.edge('q2', 'q_accept', label='ε,Z->ε')

#     elif part == 'c':
#         # PDA for the language {a^i b^j c^k | i + k = j}
#         f.edge('qi', 'q0', label='ε,ε->Z')
#         f.edge('q0', 'q0', label='a,ε->a')
#         f.edge('q0', 'q1', label='ε,ε->ε')
#         f.edge('q1', 'q1', label='b,ε->ε')
#         f.edge('q1', 'q2', label='c,a->ε')
#         f.edge('q2', 'q2', label='c,a->ε')
#         f.edge('q2', 'q_accept', label='ε,Z->ε')

#     elif part == 'g':
#         # PDA for the language {a^i b^j | i ≠ j} (Non-Deterministic)
#         f.edge('qi', 'q0', label='ε,ε->Z')
#         f.edge('q0', 'q0', label='a,ε->a')
#         f.edge('q0', 'q1', label='ε,ε->ε')
#         f.edge('q0', 'q2', label='b,ε->ε')
#         f.edge('q1', 'q1', label='b,a->ε')
#         f.edge('q1', 'q_accept', label='ε,Z->ε')
#         f.edge('q2', 'q2', label='b,ε->ε')
#         f.edge('q2', 'q_accept', label='ε,a->ε')

#     f.view()
#     return f

# # Create PDAs for parts b, c, and g
# pda_b = create_pda('b')
# pda_c = create_pda('c')
# pda_g = create_pda('g')

# # Render PDAs to JPG
# pda_b.format = 'jpg'
# pda_b.render()

# pda_c.format = 'jpg'
# pda_c.render()

# pda_g.format = 'jpg'
# pda_g.render()


from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='PDA for L = {a^i b^j | i != j}')

# Set of states
states = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6']

# Add nodes with a double circle for accepting states
for state in states:
    if state == 'q4':
        dot.node(state, state, shape='doublecircle')
    else:
        dot.node(state, state)

# Transitions for the PDA
# From q0, non-deterministically go to q1 or q2
dot.edge('q0', 'q1', label='ε,ε→$')
dot.edge('q0', 'q2', label='ε,ε→ε')

# Transitions for q1, where PDA guesses there are more a's
dot.edge('q1', 'q1', label='a,ε→X')
dot.edge('q1', 'q3', label='b,X→ε')

# Transitions for q3, go to accepting state if more b's after stack is empty
dot.edge('q3', 'q3', label='b,X→ε')
dot.edge('q3', 'q4', label='ε,$→ε')

# Transitions for q2, where PDA guesses there are more b's
dot.edge('q2', 'q2', label='a,ε→ε')
dot.edge('q2', 'q5', label='b,ε→X')

# Transitions for q5, loop reading b's and push X onto the stack
dot.edge('q5', 'q5', label='b,ε→X')
dot.edge('q5', 'q6', label='ε,ε→ε')

# Transition for q6, pop X for each ε and go to accepting state
dot.edge('q6', 'q6', label='ε,X→ε')
dot.edge('q6', 'q4', label='ε,$→ε')

# Print the graph in a PNG file
file_path = '/mnt/data/PDA_L_ai_bj_neq.png'
dot.render(file_path, view=False, format='png')


