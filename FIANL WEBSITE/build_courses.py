# -*- coding: utf-8 -*-
"""Generate 14 course detail pages from the existing course-fullstack.html
template, replacing only the course-specific zones. Boilerplate (nav, form,
stats, CTA, footer, styles) is preserved verbatim."""
import re

with open('course-fullstack.html', 'r', encoding='utf-8') as f:
    TPL = f.read()

# ---- Course content -------------------------------------------------------
# Each: file, title, badge, desc, hours, outcomes[8], modules[(name,[topics])]
COURSES = [
{
 "file":"course-graphicdesign.html","title":"Graphic Designing","badge":"🎨 All Levels",
 "desc":"Master industry-standard design tools and create stunning visuals — logos, posters, brochures and social media creatives — using Adobe Photoshop, Illustrator and InDesign.",
 "hours":60,
 "out":["Design professional logos and brand identities","Master Adobe Photoshop for photo editing","Create vector art in Adobe Illustrator","Lay out print material in Adobe InDesign","Understand colour theory and typography","Design social media and ad creatives","Build a portfolio of real design projects","Prepare print-ready and web-ready files"],
 "mod":[("Design Foundations",["Colour theory","Typography basics","Composition & layout","Design principles"]),
        ("Adobe Photoshop",["Photo editing & retouching","Layers & masks","Selections & blending","Posters & banners"]),
        ("Adobe Illustrator",["Vector fundamentals","Logo design","Icons & illustrations","Pen tool mastery"]),
        ("Adobe InDesign",["Brochures & flyers","Multi-page layouts","Print preparation","Templates"]),
        ("Portfolio & Career",["Branding project","Social media kit","Portfolio building","Freelance basics"])],
},
{
 "file":"course-java.html","title":"Java Programming","badge":"💻 All Levels",
 "desc":"Build a strong programming foundation with Core Java — from syntax and OOP to collections and exception handling — and learn to write clean, platform-independent applications.",
 "hours":48,
 "out":["Write programs using Java syntax and data types","Apply object-oriented programming concepts","Work with classes, objects and inheritance","Handle exceptions and debug effectively","Use collections and generics","Read and write files with Java I/O","Build console-based applications","Lay the foundation for full-stack/Android paths"],
 "mod":[("Java Fundamentals",["Syntax & data types","Operators & control flow","Loops & arrays","Methods"]),
        ("Object-Oriented Programming",["Classes & objects","Inheritance","Polymorphism","Encapsulation & abstraction"]),
        ("Core Libraries",["Strings & wrapper classes","Collections framework","Generics","Exception handling"]),
        ("Advanced Concepts",["File I/O","Multithreading basics","JDBC intro","Best practices"]),
        ("Project",["Mini console app","Debugging","Code review","Next steps"])],
},
{
 "file":"course-python.html","title":"Python Programming","badge":"🐍 All Levels",
 "desc":"Learn one of the world's most popular languages from scratch. Master Python syntax, data structures, functions and automation — the gateway to data science, AI and web development.",
 "hours":30,
 "out":["Write clean Python code from scratch","Work with lists, dicts, sets and tuples","Build reusable functions and modules","Handle files and exceptions","Automate repetitive tasks with scripts","Understand OOP in Python","Use popular libraries (pip ecosystem)","Prepare for data science and AI tracks"],
 "mod":[("Python Basics",["Syntax & variables","Data types","Operators","Input/output"]),
        ("Control Flow",["Conditionals","Loops","Comprehensions","Functions"]),
        ("Data Structures",["Lists & tuples","Dictionaries & sets","Strings","File handling"]),
        ("OOP & Modules",["Classes & objects","Modules & packages","Exception handling","Virtual environments"]),
        ("Automation Project",["Scripting","Working with APIs","Mini automation","Next steps"])],
},
{
 "file":"course-cpp.html","title":"C++ Programming","badge":"⚙️ All Levels",
 "desc":"Develop high-performance applications with C++. Learn OOP, memory management and the STL while building strong problem-solving and system-programming fundamentals.",
 "hours":36,
 "out":["Write efficient C++ programs","Apply OOP with classes and objects","Manage memory with pointers","Use the Standard Template Library (STL)","Handle files and streams","Solve algorithmic problems","Understand performance fundamentals","Prepare for competitive programming"],
 "mod":[("C++ Fundamentals",["Syntax & data types","Operators","Control flow","Functions"]),
        ("Object-Oriented C++",["Classes & objects","Constructors","Inheritance","Polymorphism"]),
        ("Memory & Pointers",["Pointers & references","Dynamic memory","Smart pointers","Memory safety"]),
        ("STL & Files",["Vectors & maps","Iterators & algorithms","File streams","Templates"]),
        ("Project",["Problem solving","Mini project","Debugging","Optimization"])],
},
{
 "file":"course-sql.html","title":"Database Management using SQL","badge":"🗄️ All Levels",
 "desc":"Become confident with databases. Learn to design schemas, write powerful SQL queries, and manage data — an essential skill for analysts, developers and data professionals.",
 "hours":36,
 "out":["Design normalized relational databases","Write SELECT, JOIN and subqueries","Insert, update and delete records safely","Use aggregate functions and grouping","Create tables, views and indexes","Understand transactions and constraints","Optimize queries for performance","Connect databases to applications"],
 "mod":[("Database Foundations",["Relational model","Tables & keys","Data types","Normalization"]),
        ("Querying Data",["SELECT & WHERE","ORDER BY & LIMIT","Operators","Functions"]),
        ("Joins & Aggregation",["INNER & OUTER joins","GROUP BY","HAVING","Subqueries"]),
        ("Data Management",["INSERT/UPDATE/DELETE","Views & indexes","Constraints","Transactions"]),
        ("Applied SQL",["Stored procedures intro","Reporting queries","Mini project","Best practices"])],
},
{
 "file":"course-html5.html","title":"Web Designing with HTML5","badge":"🌐 All Levels",
 "desc":"Start your web journey by building responsive, standards-compliant web pages with HTML5 and CSS3 — the foundation of every website and web application.",
 "hours":44,
 "out":["Structure pages with semantic HTML5","Style layouts with modern CSS3","Build responsive, mobile-first designs","Use Flexbox and CSS Grid","Add forms and multimedia","Apply accessibility best practices","Work with Git and version control","Publish a live multi-page website"],
 "mod":[("HTML5 Foundations",["Document structure","Semantic tags","Links & images","Lists & tables"]),
        ("Forms & Media",["Form elements","Validation","Audio & video","Embeds"]),
        ("CSS3 Styling",["Selectors & box model","Colours & typography","Backgrounds","Transitions"]),
        ("Responsive Design",["Flexbox","CSS Grid","Media queries","Mobile-first"]),
        ("Project & Deploy",["Multi-page site","Git basics","Hosting","Portfolio"])],
},
{
 "file":"course-excel.html","title":"Advanced Excel","badge":"📊 All Levels",
 "desc":"Turn spreadsheets into a superpower. Master formulas, pivot tables, dashboards and automation to analyse and present complex business data with confidence.",
 "hours":24,
 "out":["Master 50+ essential Excel formulas","Build dynamic pivot tables and charts","Create interactive dashboards","Use VLOOKUP, INDEX-MATCH and XLOOKUP","Clean and validate large datasets","Automate tasks with macros basics","Apply conditional formatting","Present data for business decisions"],
 "mod":[("Excel Essentials",["Interface & shortcuts","Formatting","Basic formulas","Data entry"]),
        ("Advanced Formulas",["Logical functions","Lookups","Text & date functions","Error handling"]),
        ("Data Analysis",["Sorting & filtering","Pivot tables","Pivot charts","Slicers"]),
        ("Dashboards",["Charts","Conditional formatting","Dynamic dashboards","KPIs"]),
        ("Automation",["Data validation","Intro to macros","Productivity tips","Case study"])],
},
{
 "file":"course-powerbi.html","title":"Power BI","badge":"📊 All Levels",
 "desc":"Transform raw data into interactive dashboards and business insights with Microsoft Power BI — one of the most in-demand business intelligence tools.",
 "hours":36,
 "out":["Connect and transform data sources","Model data with relationships","Write DAX measures and calculations","Build interactive reports and dashboards","Create compelling data visualizations","Publish and share dashboards","Apply filters, slicers and drill-downs","Tell stories with business data"],
 "mod":[("Getting Started",["Power BI overview","Data sources","Power Query","Data cleaning"]),
        ("Data Modeling",["Relationships","Star schema","Calculated columns","Intro to DAX"]),
        ("DAX & Measures",["DAX functions","Measures","Time intelligence","Context"]),
        ("Visualization",["Charts & visuals","Slicers & filters","Drill-through","Themes"]),
        ("Dashboards & Sharing",["Report design","Publishing","Workspaces","Project"])],
},
{
 "file":"course-tableau.html","title":"Tableau","badge":"📈 All Levels",
 "desc":"Create powerful, interactive data visualizations and dashboards with Tableau — the leading tool for turning data into clear, actionable visual stories.",
 "hours":36,
 "out":["Connect Tableau to multiple data sources","Build charts, maps and dashboards","Use calculated fields and parameters","Create interactive filters and actions","Design executive dashboards","Apply best practices in data viz","Publish to Tableau Public/Server","Communicate insights visually"],
 "mod":[("Tableau Basics",["Interface","Connecting data","Dimensions & measures","Basic charts"]),
        ("Building Visuals",["Bar, line & pie","Maps","Scatter & heat maps","Formatting"]),
        ("Calculations",["Calculated fields","Parameters","Table calculations","LOD basics"]),
        ("Dashboards",["Dashboard design","Filters & actions","Interactivity","Storytelling"]),
        ("Publishing",["Tableau Public","Sharing","Best practices","Project"])],
},
{
 "file":"course-tally.html","title":"Tally Essentials","badge":"💼 All Levels",
 "desc":"Master computerised accounting with TallyPrime — from company setup and vouchers to GST, payroll and financial reporting — across all three Tally Essentials levels.",
 "hours":106,
 "out":["Set up companies and chart of accounts","Record all types of accounting vouchers","Manage inventory and stock","Configure and file GST","Handle TDS, payroll and banking","Generate financial statements","Manage accounts payable/receivable","Secure and split company data"],
 "mod":[("Level 1 – Fundamentals",["Company creation","Chart of accounts","Recording transactions","Financial reports"]),
        ("Level 1 – Banking & GST",["Banking solutions","GST basics","Data security","Reports"]),
        ("Level 2 – Inventory",["Storage & classification","Order processing","Budgets","Scenario management"]),
        ("Level 2 – Payables/Receivables",["Accounts payable","Accounts receivable","GST in detail","Reporting"]),
        ("Level 3 – Advanced",["TDS","Export & import","Company data splitting","Advanced GST"])],
},
{
 "file":"course-socialmedia.html","title":"Social Media Marketing","badge":"📱 All Levels",
 "desc":"Learn to grow brands online. Master content strategy, paid ads and analytics across Facebook, Instagram, LinkedIn and more to drive real business results.",
 "hours":40,
 "out":["Build a social media marketing strategy","Create engaging content that converts","Run Facebook and Instagram ad campaigns","Grow and manage online communities","Use LinkedIn and Twitter for business","Measure performance with analytics","Plan content calendars","Generate leads and sales online"],
 "mod":[("SMM Foundations",["Platforms overview","Audience research","Brand voice","Content pillars"]),
        ("Content & Creatives",["Content planning","Copywriting","Visuals & reels","Scheduling"]),
        ("Paid Advertising",["Meta Ads Manager","Targeting","Ad creatives","Budgeting"]),
        ("Platforms Deep-Dive",["Instagram & Facebook","LinkedIn","Twitter/X","YouTube basics"]),
        ("Analytics & Strategy",["Metrics & KPIs","Reporting","Case studies","Campaign project"])],
},
{
 "file":"course-seo.html","title":"Search Engine Optimization (SEO)","badge":"🔍 All Levels",
 "desc":"Get websites to the top of Google. Learn on-page, off-page and technical SEO to drive organic traffic and improve search rankings — a high-demand digital skill.",
 "hours":18,
 "out":["Perform keyword research","Optimize on-page SEO elements","Build quality backlinks","Improve technical SEO and site speed","Use Google Search Console & Analytics","Audit and improve website SEO","Understand ranking factors","Track and report SEO performance"],
 "mod":[("SEO Foundations",["How search works","Ranking factors","Keyword research","Search intent"]),
        ("On-Page SEO",["Title & meta tags","Content optimization","Internal linking","URL structure"]),
        ("Technical SEO",["Site speed","Mobile-friendliness","Crawling & indexing","Schema basics"]),
        ("Off-Page SEO",["Backlinks","Link building","Local SEO","Authority"]),
        ("Tools & Reporting",["Search Console","Analytics","Audits","Reporting"])],
},
{
 "file":"course-foundationit.html","title":"Foundation in IT","badge":"🎓 Beginners",
 "desc":"A complete head-start in technology. Build all-round practical skills in computing, the internet, productivity software and basic programming — perfect for beginners.",
 "hours":80,
 "out":["Operate computers and operating systems confidently","Use the internet, email and cloud safely","Master MS Office productivity tools","Understand IT and information systems","Build basic web pages","Learn fundamentals of programming logic","Apply digital safety and etiquette","Prepare for advanced IT courses"],
 "mod":[("Computer Fundamentals",["Hardware & software","Operating systems","File management","Networks basics"]),
        ("Internet & Cloud",["Browsing & search","Email","Cloud storage","Online safety"]),
        ("Productivity Suite",["MS Word","MS Excel","MS PowerPoint","Outlook"]),
        ("Intro to Web",["HTML basics","Web pages","Forms","Templates"]),
        ("Programming Logic",["Logic building","Algorithms","Flowcharts","Next steps"])],
},
{
 "file":"course-webdev-csharp.html","title":"Web Development with C# & ASP.Net Core","badge":"🌐 Graduates & Professionals",
 "desc":"Build robust, enterprise-grade web applications with C# and ASP.Net Core — covering MVC, Web APIs, databases and cloud deployment for a career as a .NET developer.",
 "hours":88,
 "out":["Program confidently in C#","Build web apps with ASP.Net Core MVC","Create RESTful Web APIs","Work with Entity Framework and SQL","Implement authentication and security","Apply the MVC architecture","Deploy apps to the cloud","Build a full-stack .NET portfolio"],
 "mod":[("C# Programming",["Syntax & OOP","Collections","LINQ","Exception handling"]),
        ("ASP.Net Core Basics",["MVC architecture","Razor views","Routing","Middleware"]),
        ("Data Access",["Entity Framework Core","SQL integration","Migrations","CRUD"]),
        ("Web APIs & Security",["REST APIs","Authentication","Authorization","Validation"]),
        ("Deployment",["Cloud deployment","Configuration","Performance","Capstone project"])],
},
]

def fmt_duration(hours):
    weeks = -(-hours // 20)
    return f"{hours} Hours"

def build(course):
    c = TPL
    name = course["title"]
    # 1) <title>
    c = re.sub(r'<title>.*?</title>',
               f'<title>{name} | DVOC INSTITUTE</title>', c, count=1, flags=re.S)
    # 2) breadcrumb course name (the <span> inside .breadcrumb)
    c = re.sub(r'(<div class="breadcrumb">.*?<span>).*?(</span>)',
               lambda m: m.group(1) + name + m.group(2), c, count=1, flags=re.S)
    # 3) hero block: everything between hero-inner open and the enroll form
    pills = (f'<span class="meta-pill">⏱ {fmt_duration(course["hours"])}</span>'
             f'<span class="meta-pill">\U0001f393 Industry Certification</span>'
             f'<span class="meta-pill">\U0001f4c5 Flexible Batches</span>'
             f'<span class="meta-pill">\U0001f4bc Practical Training</span>')
    hero = (f'<div>\n      <div class="course-badge">{course["badge"]}</div>\n'
            f'      <h1>{name}</h1>\n'
            f'      <p class="hero-desc">{course["desc"]}</p>\n'
            f'      <div class="meta-pills">{pills}</div>\n    </div>\n    ')
    c = re.sub(r'(<div class="hero-inner">\s*).*?(<form class="enroll-card")',
               lambda m: m.group(1) + hero + m.group(2), c, count=1, flags=re.S)
    # 4) Learning Outcomes grid
    outs = ''.join(f'<div class="outcome-item fade-up"><div class="outcome-check">✓</div><p>{o}</p></div>'
                   for o in course["out"])
    outs_block = f'<div class="outcomes-grid">{outs}</div>\n  '
    c = re.sub(r'(<div class="section-title">Learning <span>Outcomes</span></div>\s*).*?(</div>\s*</section>)',
               lambda m: m.group(1) + outs_block + m.group(2), c, count=1, flags=re.S)
    # 5) Curriculum modules
    mods = ''
    for i, (mname, topics) in enumerate(course["mod"], 1):
        lis = ''.join(f'<li>{t}</li>' for t in topics)
        mods += (f'<div class="curr-item fade-up"><div class="curr-header">'
                 f'<span class="curr-num">Module {i:02d}</span>'
                 f'<span class="curr-title">{mname}</span>'
                 f'<span class="curr-arrow">▾</span></div>'
                 f'<ul class="curr-body">{lis}</ul></div>')
    mods_block = mods + '\n  '
    c = re.sub(r'(<div class="section-title">Full <span>Curriculum</span></div>\s*).*?(</div>\s*</section>\s*<div class="cta-section")',
               lambda m: m.group(1) + mods_block + m.group(2), c, count=1, flags=re.S)
    return c

for course in COURSES:
    out = build(course)
    with open(course["file"], 'w', encoding='utf-8', newline='') as f:
        f.write(out)
    # quick sanity
    moji = out.count('â€') + out.count('ðŸ')
    print(f'{course["file"]:32} title="{course["title"]}" badge_ok={course["badge"] in out} '
          f'outcomes={out.count("outcome-item")} modules={out.count("curr-item")} mojibake={moji}')
print("DONE: built", len(COURSES), "pages")
