from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, ListFlowable, ListItem, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from pathlib import Path

output_path = Path(__file__).resolve().parent / 'Project_Ahaa_Report.pdf'

content = []
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='TitleStyle', fontName='Helvetica-Bold', fontSize=20, leading=24, alignment=TA_CENTER, textColor=colors.HexColor('#1f4e79')))
styles.add(ParagraphStyle(name='HeadingStyle', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=colors.HexColor('#2f5597'), spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name='BodyStyle', fontName='Helvetica', fontSize=11, leading=15, alignment=TA_JUSTIFY, textColor=colors.HexColor('#222222')))
styles.add(ParagraphStyle(name='BulletStyle', fontName='Helvetica', fontSize=11, leading=14, leftIndent=18, bulletIndent=0, spaceAfter=4))

content.append(Paragraph('AI-Powered Student Project Discovery Platform', styles['TitleStyle']))
content.append(Paragraph('Project Ahaa - Detailed Technical Report', styles['BodyStyle']))
content.append(Spacer(1, 12))
content.append(Paragraph('This report explains what the project is, what it does, which packages and libraries it uses, why those tools are chosen, and how the architecture is organized.', styles['BodyStyle']))
content.append(PageBreak())

content.append(Paragraph('1. Introduction', styles['HeadingStyle']))
content.append(Paragraph('Project Ahaa is an AI-powered web-based platform developed to help students discover existing project ideas, compare them with new ideas, and get guidance on improving the project before implementation. The core aim is to reduce duplication, increase creativity, and make project planning easier for students.', styles['BodyStyle']))
content.append(Spacer(1, 6))
content.append(Paragraph('In simple terms, the project acts like a smart project discovery assistant. A user can enter a concept or idea, and the system helps by suggesting similar projects, recommending technologies, improving the idea, showing related research papers, and building a knowledge graph of the project landscape.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('2. What This Project Is Doing', styles['HeadingStyle']))
content.append(Paragraph('The project is doing three major jobs at the same time:', styles['BodyStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('It helps users discover similar or related projects from a collection of stored project records.', styles['BulletStyle'])),
    ListItem(Paragraph('It provides AI-assisted recommendations such as improvements, technologies, and research papers.', styles['BulletStyle'])),
    ListItem(Paragraph('It visualizes relationships between projects, technologies, and domains through a knowledge graph and timeline.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 8))
content.append(Paragraph('This means the project is not just a search tool. It is a complete project discovery and planning platform that supports idea generation, evaluation, and exploration.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('3. Main Features of the System', styles['HeadingStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('Project search and discovery: users can browse projects stored in the system.', styles['BulletStyle'])),
    ListItem(Paragraph('Similarity matching: similar projects are found using text embeddings and cosine similarity.', styles['BulletStyle'])),
    ListItem(Paragraph('Idea improvement: the system suggests how a student project idea can be improved or extended.', styles['BulletStyle'])),
    ListItem(Paragraph('Technology recommendations: it suggests suitable frameworks, tools, and libraries for the idea.', styles['BulletStyle'])),
    ListItem(Paragraph('Research paper suggestions: it connects the idea to academic papers through external APIs.', styles['BulletStyle'])),
    ListItem(Paragraph('Knowledge graph visualization: it creates a graph of projects, technologies, and domains.', styles['BulletStyle'])),
    ListItem(Paragraph('Timeline view: it shows how related project ideas evolved over time.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 10))

content.append(Paragraph('4. Technologies and Libraries Used', styles['HeadingStyle']))
content.append(Paragraph('The project uses a combination of frontend, backend, data science, and visualization libraries. Each library is chosen to support a specific purpose.', styles['BodyStyle']))
content.append(Spacer(1, 8))
content.append(Paragraph('Frontend libraries:', styles['BodyStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('React: used to build the interactive user interface.', styles['BulletStyle'])),
    ListItem(Paragraph('React DOM: used to render the React application in the browser.', styles['BulletStyle'])),
    ListItem(Paragraph('Axios: used to communicate with the backend API from the frontend.', styles['BulletStyle'])),
    ListItem(Paragraph('React Scripts: used to run and build the React application easily.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 6))
content.append(Paragraph('Backend libraries:', styles['BodyStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('FastAPI: used to create the API endpoints and handle HTTP requests efficiently.', styles['BulletStyle'])),
    ListItem(Paragraph('Uvicorn: used as the ASGI server to run the FastAPI app.', styles['BulletStyle'])),
    ListItem(Paragraph('Pydantic: used for request validation and schema modeling.', styles['BulletStyle'])),
    ListItem(Paragraph('Requests: used to call external APIs such as Semantic Scholar and arXiv.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 6))
content.append(Paragraph('AI and data processing libraries:', styles['BodyStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('NumPy: used for numerical operations, especially vector and matrix calculations.', styles['BulletStyle'])),
    ListItem(Paragraph('Scikit-learn: used for cosine similarity and vector-based matching.', styles['BulletStyle'])),
    ListItem(Paragraph('Sentence Transformers: used to generate text embeddings that represent the meaning of project descriptions.', styles['BulletStyle'])),
    ListItem(Paragraph('NetworkX: used to build and manage the knowledge graph structure.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 6))
content.append(Paragraph('Why these libraries are used:', styles['BodyStyle']))
content.append(Paragraph('The frontend libraries are chosen because the application is a modern web app that needs a smooth and responsive UI. The backend libraries are chosen for speed, simplicity, and ease of API development. The AI libraries are chosen because the project depends on text understanding, semantic similarity, and graph-based relations.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('5. Project Architecture', styles['HeadingStyle']))
content.append(Paragraph('The system follows a simple three-layer architecture:', styles['BodyStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('Presentation layer: the React frontend provides all user interaction and visualization.', styles['BulletStyle'])),
    ListItem(Paragraph('Application layer: the FastAPI backend processes requests and connects the frontend to the AI modules.', styles['BulletStyle'])),
    ListItem(Paragraph('Data layer: JSON files store project records and the technology knowledge base.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 8))
content.append(Paragraph('The architecture is modular. Each feature is placed in a separate Python module so that the system is easier to maintain and expand. The API layer acts as the central coordinator that connects user requests to the appropriate logic module.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('6. How the System Works', styles['HeadingStyle']))
content.append(Paragraph('A typical workflow is as follows:', styles['BodyStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('The user opens the app and enters a project idea or keyword.', styles['BulletStyle'])),
    ListItem(Paragraph('The frontend sends the request to the FastAPI backend.', styles['BulletStyle'])),
    ListItem(Paragraph('The backend calls the relevant function such as similarity search or idea improvement.', styles['BulletStyle'])),
    ListItem(Paragraph('The AI module processes the input and returns recommendations or graph data.', styles['BulletStyle'])),
    ListItem(Paragraph('The frontend displays the results in a user-friendly view.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 8))
content.append(Paragraph('For example, when a student searches for a project idea, the system converts the request into a vector representation, compares it with existing project data, and returns the most similar entries. This makes it easier to see whether the idea already exists or whether it can be improved.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('7. Why the Project Is Designed This Way', styles['HeadingStyle']))
content.append(Paragraph('The design is simple because the project is mainly a prototype and academic demonstration platform. A lightweight architecture is better here than a large production system because it makes the project easier to understand, run, and improve. The use of JSON files instead of a full database keeps setup easy and suitable for local development.', styles['BodyStyle']))
content.append(Spacer(1, 6))
content.append(Paragraph('The project also uses fallback logic for recommendations. This means that even if an external API is unavailable, the app can still provide useful outputs through local rules or keyword matching. That improves robustness and makes the system more practical for students.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('8. Strengths of the Project', styles['HeadingStyle']))
content.append(ListFlowable([
    ListItem(Paragraph('Clear separation between frontend, backend, and AI logic.', styles['BulletStyle'])),
    ListItem(Paragraph('User-friendly interface for project discovery.', styles['BulletStyle'])),
    ListItem(Paragraph('Good support for idea improvement and guidance.', styles['BulletStyle'])),
    ListItem(Paragraph('Can function even when external APIs are limited.', styles['BulletStyle'])),
], bulletType='bullet'))
content.append(Spacer(1, 10))

content.append(Paragraph('9. Possible Improvements', styles['HeadingStyle']))
content.append(Paragraph('The project can be improved further by integrating a real database, using environment variables for secrets, improving the UI design, and adding user authentication. These improvements would make the platform more scalable and suitable for real-world deployment.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('10. Conclusion', styles['HeadingStyle']))
content.append(Paragraph('Project Ahaa is a smart project discovery and idea planning platform that combines AI, web development, and data visualization. It is designed to assist students by helping them discover similar projects, improve ideas, find relevant technologies, and explore research literature. The architecture is modular, practical, and well suited for educational and prototype use.', styles['BodyStyle']))
content.append(Spacer(1, 10))

content.append(Paragraph('11. Key Project Files', styles['HeadingStyle']))
table_data = [
    ['File', 'Role'],
    ['backend/main.py', 'Main FastAPI application and API routes'],
    ['backend/similarity_engine.py', 'Similarity search using embeddings'],
    ['backend/idea_improver.py', 'Improvement suggestions for project ideas'],
    ['backend/tech_recommender.py', 'Technology recommendations'],
    ['backend/paper_recommender.py', 'Research paper suggestions'],
    ['backend/knowledge_graph.py', 'Knowledge graph construction'],
    ['frontend/src/App.js', 'Main React application interface'],
]

table = Table(table_data, repeatRows=1, hAlign='LEFT')
table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#d9eaf7')),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
]))
content.append(table)

pdf = SimpleDocTemplate(str(output_path), pagesize=A4, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
pdf.build(content)
print(f'PDF created: {output_path}')
