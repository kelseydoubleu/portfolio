# Portfolio content. Edit text here, then run:  python3 _src/build.py
# Images live in /img. Captions are optional.

SITE = {
    "name": "KELSEY WANG",
    "tagline": "Architectural designer and technologist in New York. I build games, tools and drawings that make hidden systems legible.",
    "links": [
        ("GitHub", "https://github.com/kelseydoubleu"),
        ("PDF portfolio", "book/"),
    ],
}

ABOUT = [
    "Kelsey Wang is an architectural designer and creative technologist based in Brooklyn. She holds an M.Arch from Columbia GSAPP (2026) and a computer science background from Stanford.",
    "She works in the Design Technology studio at Gensler New York, building data products and tools for design teams. She also holds a research appointment with Professor Amelyn Ng at Columbia, working on machine perception, object detection and drawing, and teaches at GSAPP.",
    "Her work sits between architecture and software: playable simulations of how cities decide, websites that act as public instruments, and drawings that follow a thing from origin to consequence.",
]

CV = [
    ("Education", [
        ("2023-2026", "Master of Architecture, Columbia GSAPP"),
        ("", "Computer Science, Stanford University"),
    ]),
    ("Work", [
        ("2026-", "Design Technology, Gensler New York"),
        ("2026-", "Research appointment, Columbia GSAPP (with Amelyn Ng)"),
        ("2026-", "Teaching Associate, Columbia GSAPP"),
    ]),
]

# section: studio | research | play
PROJECTS = [
    {
        "slug": "after-leisure", "section": "studio",
        "title": "AFTER LEISURE",
        "meta": [("Semester", 'ADV IV "Sanctuaries Territories", Spring 2025'), ("Site", "Sleepy Hollow Country Club, Hudson Valley, NY"),
                 ("Partner", "Hannah Zhao"), ("Instructor", "Nahyun Hwang")],
        "summary": "A private country club reimagined as a shared landscape of ecological, social and spatial repair.",
        "cover": "al-pots",
        "body": [
            "This project reimagines Sleepy Hollow Country Club as a fractured landscape of ecological, social and spatial repair. Once upheld by exploitative labor systems and elite leisure, the site becomes a testing ground for new land stewardship models built on care, conflict and collaboration.",
            "After Leisure examines the hidden labor and ecological systems that sustain an exclusive recreational landscape. Using the golf club as a case study, the project maps the asymmetry between visible enjoyment and invisible maintenance. Leisure is framed not as neutral pleasure but as an economy structured by wages, seasonal work, land management and environmental extraction.",
        ],
        "sections": [
            ("The labor network", [
                "The labor network diagram maps the full actor ecosystem sustaining the club's \"sanctuary\": dollar amounts and hourly wages tracing the economic gradient hidden beneath the experience of escape.",
                "The Land & Leisure Trust is presented as a speculative website: a public-facing instrument through which the site's restructuring is proposed, phased and explained by the voices of the workers who actually maintain it.",
            ], ["al-labor", "al-trust"]),
            ("Rewriting the fairway", [
                "Fairways and manicured terrain are rewritten as shared landscapes of cultivation, gathering and ecological repair. Soil banks, communal kitchens, classroom pavilions, greenhouse towers and slow-growing clover meadows redistribute access while rebalancing the site's maintenance cycles.",
            ], ["al-strip", "al-pots", "al-pavilion", "al-meadow", "al-greenhouse"]),
            ("Leisure as participation", [
                "Leisure is restructured as participation: planting, cooking, learning and gathering become shared acts that redistribute both access and care. Rather than erasing the site's past as an exclusive recreational landscape, the proposal makes its systems visible and negotiable.",
            ], ["al-model", "al-grid"]),
        ],
        "links": [],
    },
    {
        "slug": "by-product", "section": "studio",
        "title": "BY/PRODUCT",
        "meta": [("Semester", 'ADV VI "Design As Research", Spring 2026'), ("Type", "Thesis"), ("Instructor", "Lydia Kallipoliti")],
        "summary": "A method for reading the value systems embedded in what we build, before machines inherit them.",
        "cover": "bp-site",
        "body": [
            "Every made thing leaves a byproduct. A cut produces an offcut. A stone block requires a quarry. A microchip exploits bodily labor. The product is designed to perfection. The byproduct rarely is.",
            "This thesis proposes a methodology for reading the value systems embedded in what we build, before they are inherited by the machines about to dictate the next century. AI is an act of archival. Whatever we feed it becomes the canon, reproduced at a scale no individual architect ever could. A building that externalizes its waste, conceals its labor and has no plan for its own death carries a value system that will be passed down to every model trained on it.",
            "The most urgent task we have as designers is to learn how to follow a thing from origin to consequence, and ask whether its maker planned for the aftereffects. Most have not. BY/PRODUCT asks what it would look like if they had.",
        ],
        "sections": [
            ("The H100", [
                "The H100 is the most deliberate object ever made. Its transistors are measured in nanometers. Nothing that comes out of it was designed at all. The supply chain ends where consequences begin (silicosis, leukemia clusters, drained aquifers, engineered obsolescence), distributed across everyone who never signed the transaction.",
                "When severity is plotted against scale, the data resolves into a predictable curve. All except the outliers: men whose personal accumulation exceeds the GDP of most nations, built on labor priced at the margin.",
            ], ["bp-curve", "bp-chain"]),
            ("Offset Island", [
                "To build anything, you deplete a natural resource. Every beam requires a tree that once stood. Every foundation generates waste that must go somewhere. The island is finite, and the players must constantly cope with that.",
            ], ["bp-island", "bp-island-3d"]),
            ("Constitutions", [
                "What a system does with its waste, its labor and its death is its constitution. The wasp nest, the Ise Shrine, the coral reef. One dissolves on schedule. One rebuilds every twenty years. One leaves its dead as foundation.",
            ], ["bp-constitution", "bp-book"]),
        ],
        "links": [("Play Offset Island", "https://offsetisland.space"), ("Read the Constitution Reader", "https://kelseydoubleu.github.io/constitutionreader/")],
    },
    {
        "slug": "carbon-temples", "section": "studio",
        "title": "CARBON TEMPLES",
        "meta": [("Semester", 'ADV V "Scaling Up", Fall 2025'), ("Site", "125th Street, East Harlem, NYC"),
                 ("Partner", "Lorennah Granfors"), ("Instructor", "David Benjamin")],
        "summary": "A network of civic architectures that make carbon sequestration visible, participatory and desirable.",
        "cover": "ct-section",
        "body": [
            "Cities sanctify consumption through storefronts, monuments and transit infrastructure. Carbon Temples asks why carbon cannot be sanctified the same way.",
            "Today, sustainability falls on individual guilt: count your footprint, offset your latte. The real responsibility should sit with systems and corporations. What if architecture itself became a carbon bank? What if prestige shifted from money and glass facades to carbon hoards? Climate change is a failure of attention and desire as much as of systems. The project proposes a network of civic architectures that make sequestration visible, participatory and desirable across the 125th Street corridor.",
        ],
        "sections": [
            ("Four sites of carbon conviction", [
                "A circular economy coffee shop, a church, a train station and the Museum of Carbon. Each one is a familiar institution re-coded as a space where sequestration is visible, participatory and collectively valued. Carbon becomes the program.",
            ], ["ct-network", "ct-temples", "ct-axon"]),
            ("The Museum of Carbon", [
                "The Museum of Carbon is the culmination of a biomaterial research process that began with spent coffee grounds and straw waste. Carbon leaves a mark. The same waste that forms the structure also forms the brand and the accounting system: a space where carbon is stored, displayed, adopted and collectively valued. Architecture as an instrument for driving up carbon conviction.",
            ], ["ct-section", "ct-material"]),
            ("Carbon Capital, the game", [
                "Can four players change a city's mind? Carbon Capital is a playable simulation of the same 125th Street blocks. A Policymaker, a Developer, an Architect and a Citizen each chase their own score (approval, profit, recognition, livability) while sharing two numbers: a carbon budget that runs out at 100,000 tons and a conviction index that fades every round.",
                "Low-carbon moves unlock the four temples and, eventually, a Material Hub that grows the street's own building material. Win together by reaching 80% conviction with the Hub running, or let the budget run out. Play alone against three computer players or pass the screen between four people.",
            ], ["cc-game"]),
        ],
        "links": [("Play Carbon Capital", "https://kelseydoubleu.github.io/CarbonCapital/")],
    },
    {
        "slug": "spectacle-sh-216", "section": "studio",
        "title": "SPECTACLE & SH-216",
        "meta": [("Semester", 'Core II "Damage Control", Spring 2024'), ("Site", "Hart Senate Office Building, SH-216 (The Central Hearing Facility)"),
                 ("Instructor", "Maria Alejandra Linares Trelles")],
        "summary": "The Congressional hearing room, redesigned as the stage it already is.",
        "cover": "sp-axon",
        "body": [
            "The American Congressional Hearing Room is designed for democracy and transparency. It produces spectacle. Senators stage confrontations for cameras. Witnesses perform contrition. Wood-paneled walls and marble backdrops lend institutional legitimacy to what are, more often than not, performances for an audience that is not in the room.",
            "Rather than resist this, the project embraces it. If the hearing has become media, the room should be designed as a set: with workrooms for Congress, a red carpet for the witnesses, confessional filming areas, VIP commentary booths open to the public, and overflow seating for watching outside the hearing facility.",
        ],
        "sections": [
            ("Four modes of exchange", [
                "To stress test the framework, four spatial arrangements were developed, each corresponding to a different mode of information exchange: conversational, confrontational, rotational and instructional. These proto-interventions challenge what a Congressional hearing room should look like, and remind us how much the room shapes what can be said in it.",
            ], ["sp-renders", "sp-diagram"]),
            ("The set", [], ["sp-axon", "sp-hero", "sp-model"]),
        ],
        "links": [],
    },
    {
        "slug": "where-objects-rest", "section": "studio",
        "title": "WHERE OBJECTS REST",
        "meta": [("Semester", 'Core III "Every Thing, A Home", Fall 2024'), ("Site", "454-458 W 128th St, New York, NY"), ("Instructor", "Jelisa Blumberg")],
        "summary": "Housing designed equally for people and for their objects.",
        "cover": "wo-plan",
        "body": [
            "Housing is typically designed for people. This project proposes one designed equally for their objects. A central storage core organizes circulation while serving as a shared archive for residential belonging, inspired by the Metabolist movement, where the core remains constant while the surroundings evolve.",
            "Sir John Soane's drawing office, where objects are not hidden but displayed, studied and lived among, is the project's reference. Units are designed around what residents keep: storage becomes a spatial and social layer rather than a closet.",
        ],
        "sections": [
            ("Units", [], ["wo-studio", "wo-2bdr", "wo-1bdr", "wo-soane"]),
            ("Levels", [], ["wo-levels"]),
            ("Scripted density", [
                "A Grasshopper script automates the placement of modular housing units across a site based on adjustable building heights and density goals. Each iteration evaluates FAR, unit count and storage capacity, supporting rapid exploration of housing and development scenarios.",
            ], ["wo-script"]),
        ],
        "links": [],
    },
    {
        "slug": "125-corner-university", "section": "studio",
        "title": "125 CORNER UNIVERSITY",
        "meta": [("Semester", 'Core I "Fugitive Mobilities", Fall 2023'), ("Site", "Harlem, NYC"), ("Instructor", "Galen Pardee")],
        "summary": "A big-box retail building returned to its original civic mission.",
        "cover": "cu-axon",
        "body": [
            "Originally built in 2001 by the Abyssinian Development Corporation as a big box retail and office complex, 125 Corner University reimagines the building as a vertical neighborhood institution that serves every member of the Harlem community within a single structure.",
            "The Abyssinian Development Corporation built this building to rebuild the social and physical capital of Harlem. What opened was a Marshalls, a CVS and a Dunkin Donuts. 125 Corner University returns the building to that original mission, stacking the services the community actually needs above the retail that pays for them.",
        ],
        "sections": [
            ("", [], ["cu-hero", "cu-collage", "cu-stack", "cu-context"]),
        ],
        "links": [],
    },
    # ---------- research ----------
    {
        "slug": "bounding-box-architecture", "section": "research",
        "title": "BOUNDING BOX ARCHITECTURE",
        "meta": [("Type", "Research, 2026"), ("With", "Amelyn Ng, Columbia GSAPP"), ("Tools", "YOLO11 / YOLO12, ONNX Runtime Web, Supabase")],
        "summary": "A machine vision probe: what object detection sees in architecture, and what dissolves into noise.",
        "cover": "bb-og",
        "body": [
            "How we design our data is how we design our outputs. Bounding Box Architecture is a machine vision probe for architectural images. Upload a photograph, a rendering or a collage, and object detection models report what they recognize. Everything the model has no word for dissolves into noise.",
            "People then label what the model missed, and those labels build a shared archive of the built environment's blind spots. Detection runs entirely in the browser, so images only leave the device when someone chooses to save them. The site was used in a workshop with about 120 students uploading images from their phones.",
        ],
        "sections": [],
        "links": [("Try it", "https://boundingboxarchitecture.site/"), ("Code", "https://github.com/kelseydoubleu/bounding-box-architecture")],
    },
    {
        "slug": "offbrand-assets", "section": "research",
        "title": "OFFBRAND ASSETS",
        "meta": [("Type", "Research, 2026"), ("With", "Amelyn Ng, Columbia GSAPP"), ("Tools", "Revit, Dynamo, Python")],
        "summary": "Alt-generic Revit families: generic in build, specific in life.",
        "cover": None,
        "body": [
            "BIM libraries are full of generic furniture: the default bed, the default dining table, the same six chairs. Offbrand Assets is a set of downloadable, parametric \"stick\" Revit families that stay generic in how they are built but become specific in what they show.",
            "The bed comes in types like Bed Rot, Pillow Lover, Never Makes Bed, Sick Day, Laundry Day and Hotel. The dining table holds Lunar New Year before and after the meal, Thanksgiving, homework time, a poker game and a house party. Seats, bed size, pizza count and laundry amount are parameters. The project is framed against the standardizing logic of the Frankfurt Kitchen.",
        ],
        "sections": [],
        "links": [],
    },
    # ---------- play ----------
    {
        "slug": "carbon-capital", "section": "play", "external": "https://kelseydoubleu.github.io/CarbonCapital/",
        "title": "CARBON CAPITAL", "summary": "A four-player simulation of 125th Street. Win alone, or win together.", "cover": "cc-game",
        "meta": [("From", "Carbon Temples, ADV V")],
    },
    {
        "slug": "offset-island", "section": "play", "external": "https://offsetisland.space",
        "title": "OFFSET ISLAND", "summary": "Every beam requires a tree. The island is finite.", "cover": "bp-island",
        "meta": [("From", "BY/PRODUCT, ADV VI")],
    },
    {
        "slug": "constitution-reader", "section": "play", "external": "https://kelseydoubleu.github.io/constitutionreader/",
        "title": "CONSTITUTION READER", "summary": "What a system does with its waste, labor and death.", "cover": "bp-constitution",
        "meta": [("From", "BY/PRODUCT, ADV VI")],
    },
    {
        "slug": "bounding-box-tool", "section": "play", "external": "https://boundingboxarchitecture.site/",
        "title": "BOUNDING BOX", "summary": "Run object detection on any architectural image, in your browser.", "cover": "bb-og",
        "meta": [("From", "Research with Amelyn Ng")],
    },
]

SECTIONS = [("studio", "Studio work, GSAPP 2023-2026"), ("research", "Research"), ("play", "Games + tools")]
