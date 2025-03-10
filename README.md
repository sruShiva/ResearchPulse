# ResearchPulse

This repository contains the hackathon submission for "Building the Next-Gen Agentic App with GraphRAG & NVIDIA cuGraph." The submission includes the following files:

1. **Colab Notebook** - A walkthrough and step-by-step guide for the agentic app.
2. **Demo Code** - The code for the app's demo.
3. **PowerPoint Presentation** - A detailed presentation outlining the business problem and the proposed solution.
   
## Agents used to achieve results:
1. text_to_aql_to_text – Transforms natural language into AQL queries and converts the results back into text.  
2. text_to_nx_algorithm_to_text – Interprets natural language to apply specialized NetworkX algorithms and returns the results.  
3. analyse_networkx – Performs graph analysis from a stakeholder perspective using advanced data analytics algorithms and provides insights.  
4. visualize_graph – Generates visual representations of graph analytics for better interpretation.

## Instructions for the app:

   To the run the app:
  - **Frontend**: Navigate to the *frontend* folder and run `npm start` to launch the frontend.
  - **Backend**: Go to the *backend* folder and execute `python main.py` to run the backend.
  
  The backend contains:
  - **Personas folder**: Includes code for the student, professor, and benefactor personas.
  - **Utilities folder**: Contains code for the ArangoDB database and helper functions.

## About the Solution:
The solution aims to create an ecosystem for research that brings together students, professors, and benefactors (who fund research) under one unified platform. We have built agentic apps tailored to address the needs of each persona within this ecosystem.

Assumptions Made for the App (Demo):
1. Limited Dataset: Due to the restricted dataset, we have assumed the European institution to be the University of Oxford. All answers are provided based on this assumption.
2. The app enriches data with external insights, providing relevant solutions to all three personas. This helps increase collaboration and facilitates sound decision-making across the research ecosystem.


## Features of the app:
1. Unified platform:
   
![image](https://github.com/user-attachments/assets/b689817a-e2f0-483c-a010-1585939056b7)

2. Tailored set of Q&A for each persona and suggestive questions to give them a headstart:
 
![image](https://github.com/user-attachments/assets/d5b2c22a-6baf-4760-8626-9a3ef84bce4a)

3. Q&A support to answer all questions
   
![image](https://github.com/user-attachments/assets/a41b36b9-c89b-4105-9509-1310c61da8b7)

4. Viusalition capabilities for better analytics:
![image](https://github.com/user-attachments/assets/c8114fdb-7eed-4eb4-b357-b068a31b5e16)











