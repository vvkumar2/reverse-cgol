import streamlit as st

def show_writeup():
    st.title("Reversing Conway's Game of Life States")

    st.markdown("#### Initial Approach: Simulated Annealing and Genetic Algorithms")
    st.write("""
        The quest to reverse the states of Conway's Game of Life initially led me to explore simulated annealing and genetic algorithms, both renowned for their robust solution-finding capabilities in complex spaces. Simulated annealing is particularly inspired by the metallurgical process of annealing, where materials are heated and then allowed to cool slowly to minimize their internal stresses. In computational terms, this method starts with a high 'temperature,' allowing the algorithm to explore the solution space freely, even accepting suboptimal solutions to avoid local minima. As the temperature is gradually lowered, the algorithm refines its search, focusing increasingly on areas near the best solutions found. Despite its potential, simulated annealing was inefficient for our needs due to the long computational times required for convergence, especially problematic given the large and complex grids involved in the Game of Life.
                
        Similarly, genetic algorithms emulate the process of natural evolution, using techniques such as mutation, crossover, and selection to evolve a population of solutions over time. Each solution is evaluated based on a fitness function, which in our case, measured how closely a given state matched the desired outcome when evolved according to the rules of the Game of Life. Although this method showed promise, its stochastic nature often failed to consistently produce perfect results. In tasks requiring precise configurations, such as forming words from Game of Life patterns, even minor inaccuracies could lead to unsatisfactory outcomes.
    """)

    st.markdown("#### Transition to SAT Solvers")
    st.write("""
        Given the limitations of heuristic methods, my strategy pivoted towards the deterministic approach provided by SAT solvers. SAT solvers, which are algorithms designed to solve the Boolean satisfiability problem, determine if there exists an assignment to variables that makes a given Boolean formula true. This approach is ideally suited for problems like reversing the Game of Life, where each cell’s state can be represented as a Boolean variable, and the evolution rules can be translated into a series of logical constraints.

        Kissat, a state-of-the-art SAT solver, was chosen for its efficiency in handling complex satisfiability problems. Accompanying Kissat in this endeavor was the tool SBVA (Structured Bounded Variable Addition), which significantly enhances the solver’s ability to manage large sets of clauses by introducing additional structured variables. This helps simplify the complexity inherent in the SAT formulations of the Game of Life, where clauses can reach into the hundreds of thousands.
    """)

    st.markdown("#### Optimization")
    st.write("""
        Of the few solvers I had seen, most could usually only reverse a 20x20 grid about 3 times, depending on the final state complexity, before they were too much for the SAT solvers to handle. I wanted to beat this.
            
        First, I was able to optimize this application by using the Kissat/SBVA duo (rather than Z3, Glucose and other weaker SAT solvers).

        To refine the solution further and provide nicer looking output, I implemented targeted rules focusing on cellular neighborhoods. The 'One Neighbor Rule' ensures that dead cells with no live neighbors remain dead in the previous state, helping to prevent random live cells from corrupting the intended pattern. This rule significantly reduces the complexity of the SAT problem by eliminating unnecessary variables and clauses. If this results in an unsatisfiable set of conditions, I then relax the constraint a little bit more to consider second-degree neighbors, allowing a more flexible solution space that can often resolve to a satisfiable state even when tighter constraints fail.
             
        These are some of the optimizations I made for my solver to be able to reverse a 20x20 grid about 6-7 times.
    """)

    st.markdown("#### Applications")
    st.write("""
        Obviously, users can just input a specific Game of Life configuration and reverse it to find the earliest possible state that would evolve into the given pattern.
             
        However, I also created a unique font that converts text into Game of Life configurations, allowing users to input words and phrases and see them rendered as evolving cellular automata. This innovative application not only demonstrates the practical capabilities of the reverse engineering process but also offers a more entertaining way for inexperienced users to interact with and appreciate the complexities of cellular automata.        
    """)

    st.markdown("#### Conclusion")
    st.write("""
        The exploration of reversing the states of Conway's Game of Life from heuristic approaches to a structured SAT solver-based methodology illustrates the critical importance of algorithm selection tailored to specific problem characteristics. By leveraging advanced computational techniques and integrating creative optimizations, this project successfully achieves both reliable solutions and visually appealing results, showcasing the powerful intersection of computational science and creative application.
    """)

if __name__ == "__main__":
    show_writeup()
