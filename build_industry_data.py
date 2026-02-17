"""Generate industry_data.json from curated company data."""
import json

def c(name, domain, desc, funding, stage, founded, hq):
    return {"name": name, "domain": domain, "description": desc, "funding": funding, "stage": stage, "founded": founded, "hq": hq}

def sub(id, name, companies):
    return {"id": id, "name": name, "companies": companies}

def ind(id, name, subs):
    return {"id": id, "name": name, "sub_industries": subs}

industries = [
    # ── 1. AI & ML ──
    ind("ai-ml", "Artificial Intelligence & Machine Learning", [
        sub("generative-ai", "Generative AI & LLMs", [
            c("OpenAI", "openai.com", "Creator of GPT and ChatGPT", "$11.3B", "Late", 2015, "San Francisco, CA"),
            c("Anthropic", "anthropic.com", "AI safety company behind Claude", "$7.6B", "Late", 2021, "San Francisco, CA"),
            c("Cohere", "cohere.com", "Enterprise-focused large language models", "$970M", "Late", 2019, "Toronto, Canada"),
            c("Mistral AI", "mistral.ai", "Open-weight European LLM developer", "$640M", "Growth", 2023, "Paris, France"),
            c("AI21 Labs", "ai21.com", "Enterprise AI with Jamba language models", "$336M", "Growth", 2017, "Tel Aviv, Israel"),
            c("Stability AI", "stability.ai", "Open-source generative AI for images and text", "$264M", "Growth", 2019, "London, UK"),
            c("Character.ai", "character.ai", "Conversational AI characters platform", "$193M", "Growth", 2021, "Menlo Park, CA"),
            c("Hugging Face", "huggingface.co", "Open-source AI model hub and tools", "$395M", "Late", 2016, "New York, NY"),
            c("Writer", "writer.com", "Enterprise generative AI platform for content", "$326M", "Growth", 2020, "San Francisco, CA"),
            c("Jasper", "jasper.ai", "AI content creation for marketing teams", "$131M", "Growth", 2021, "Austin, TX"),
        ]),
        sub("computer-vision", "Computer Vision", [
            c("Scale AI", "scale.com", "Data labeling and AI infrastructure platform", "$1.6B", "Late", 2016, "San Francisco, CA"),
            c("Tractable", "tractable.ai", "AI visual assessment for insurance and auto", "$115M", "Growth", 2014, "London, UK"),
            c("Placer.ai", "placer.ai", "Location analytics and foot traffic intelligence", "$118M", "Growth", 2016, "Los Altos, CA"),
            c("Clarifai", "clarifai.com", "Enterprise computer vision and NLP platform", "$100M", "Growth", 2013, "Washington, DC"),
            c("Landing AI", "landing.ai", "Visual inspection AI for manufacturing", "$64M", "Growth", 2017, "Palo Alto, CA"),
            c("Viso.ai", "viso.ai", "No-code computer vision application platform", "$27M", "Early", 2018, "Fribourg, Switzerland"),
        ]),
        sub("mlops-infra", "MLOps & AI Infrastructure", [
            c("Databricks", "databricks.com", "Unified data analytics and AI platform", "$4.2B", "Late", 2013, "San Francisco, CA"),
            c("Weights & Biases", "wandb.ai", "ML experiment tracking and model management", "$250M", "Growth", 2017, "San Francisco, CA"),
            c("Anyscale", "anyscale.com", "Scalable AI compute built on Ray", "$259M", "Growth", 2019, "San Francisco, CA"),
            c("Together AI", "together.ai", "Cloud platform for running open-source AI models", "$425M", "Growth", 2022, "San Francisco, CA"),
            c("Replicate", "replicate.com", "Run AI models via API in the cloud", "$58M", "Growth", 2019, "San Francisco, CA"),
            c("Modal", "modal.com", "Serverless cloud for AI and data workloads", "$64M", "Growth", 2021, "New York, NY"),
            c("CoreWeave", "coreweave.com", "GPU cloud provider for AI workloads", "$1.6B", "Late", 2017, "Roseland, NJ"),
            c("Lambda", "lambdalabs.com", "GPU cloud infrastructure for AI training", "$320M", "Growth", 2012, "San Francisco, CA"),
        ]),
        sub("conversational-ai", "Conversational AI & NLP", [
            c("Rasa", "rasa.com", "Open-source conversational AI framework", "$70M", "Growth", 2016, "San Francisco, CA"),
            c("LivePerson", "liveperson.com", "Enterprise conversational AI platform", "Public", "Public", 1995, "New York, NY"),
            c("Ada", "ada.cx", "AI-powered customer service automation", "$190M", "Growth", 2016, "Toronto, Canada"),
            c("Kore.ai", "kore.ai", "Enterprise virtual assistant platform", "$173M", "Growth", 2013, "Orlando, FL"),
            c("Yellow.ai", "yellow.ai", "Enterprise conversational AI for CX automation", "$102M", "Growth", 2016, "San Mateo, CA"),
            c("Observe.AI", "observe.ai", "AI for contact center intelligence", "$214M", "Growth", 2017, "San Francisco, CA"),
        ]),
        sub("vertical-ai", "Vertical & Applied AI", [
            c("Palantir", "palantir.com", "AI platforms for government and enterprise", "Public", "Public", 2003, "Denver, CO"),
            c("C3.ai", "c3.ai", "Enterprise AI application platform", "Public", "Public", 2009, "Redwood City, CA"),
            c("DataRobot", "datarobot.com", "Automated machine learning platform", "$1B", "Late", 2012, "Boston, MA"),
            c("H2O.ai", "h2o.ai", "Open-source AI and ML platform", "$251M", "Growth", 2012, "Mountain View, CA"),
            c("Uniphore", "uniphore.com", "AI for enterprise customer experience", "$610M", "Late", 2008, "Palo Alto, CA"),
            c("Abnormal Security", "abnormalsecurity.com", "AI-based email security platform", "$284M", "Growth", 2018, "San Francisco, CA"),
        ]),
    ]),

    # ── 2. Fintech ──
    ind("fintech", "Fintech", [
        sub("payments", "Payments & Digital Wallets", [
            c("Stripe", "stripe.com", "Online payment processing infrastructure", "$8.7B", "Late", 2010, "San Francisco, CA"),
            c("Checkout.com", "checkout.com", "Global payment processing platform", "$1.8B", "Late", 2012, "London, UK"),
            c("Brex", "brex.com", "Corporate cards and spend management for startups", "$1.2B", "Late", 2017, "San Francisco, CA"),
            c("Marqeta", "marqeta.com", "Modern card issuing and payment platform", "Public", "Public", 2010, "Oakland, CA"),
            c("Flutterwave", "flutterwave.com", "African payment infrastructure", "$474M", "Late", 2016, "San Francisco, CA"),
            c("Rapyd", "rapyd.net", "Global fintech-as-a-service platform", "$770M", "Late", 2016, "London, UK"),
            c("Adyen", "adyen.com", "Global payments platform for enterprises", "Public", "Public", 2006, "Amsterdam, Netherlands"),
            c("dLocal", "dlocal.com", "Emerging markets payment processing", "Public", "Public", 2016, "Montevideo, Uruguay"),
        ]),
        sub("neobanking", "Neobanking & Digital Banking", [
            c("Chime", "chime.com", "Fee-free mobile banking for consumers", "$2.3B", "Late", 2012, "San Francisco, CA"),
            c("Revolut", "revolut.com", "Global neobank and financial super app", "$1.7B", "Late", 2015, "London, UK"),
            c("Nubank", "nubank.com.br", "Latin America's largest digital bank", "Public", "Public", 2013, "Sao Paulo, Brazil"),
            c("N26", "n26.com", "European mobile banking platform", "$1.7B", "Late", 2013, "Berlin, Germany"),
            c("Monzo", "monzo.com", "UK digital bank with smart money management", "$890M", "Late", 2015, "London, UK"),
            c("Current", "current.com", "Mobile banking for underserved Americans", "$400M", "Growth", 2015, "New York, NY"),
            c("Varo", "varomoney.com", "Digital bank with no minimum balances", "$992M", "Late", 2015, "San Francisco, CA"),
        ]),
        sub("lending-credit", "Lending & Credit", [
            c("Klarna", "klarna.com", "Buy now, pay later payments platform", "$4.6B", "Late", 2005, "Stockholm, Sweden"),
            c("Affirm", "affirm.com", "Buy now, pay later consumer lending", "Public", "Public", 2012, "San Francisco, CA"),
            c("Upstart", "upstart.com", "AI-powered consumer lending platform", "Public", "Public", 2012, "San Mateo, CA"),
            c("Figure", "figure.com", "Blockchain-based lending and financial services", "$558M", "Late", 2018, "San Francisco, CA"),
            c("Creditas", "creditas.com", "Brazilian secured consumer lending platform", "$829M", "Late", 2012, "Sao Paulo, Brazil"),
            c("Funding Circle", "fundingcircle.com", "Small business lending marketplace", "Public", "Public", 2010, "London, UK"),
        ]),
        sub("wealth-management", "Wealth Management & Investing", [
            c("Robinhood", "robinhood.com", "Commission-free stock and crypto trading", "Public", "Public", 2013, "Menlo Park, CA"),
            c("Wealthfront", "wealthfront.com", "Automated investment management", "$205M", "Late", 2008, "Palo Alto, CA"),
            c("Betterment", "betterment.com", "Robo-advisor for automated investing", "$435M", "Late", 2008, "New York, NY"),
            c("Public.com", "public.com", "Social investing and alternative assets platform", "$310M", "Growth", 2019, "New York, NY"),
            c("Titan", "titan.com", "Actively managed investment platform", "$101M", "Growth", 2018, "New York, NY"),
            c("Acorns", "acorns.com", "Micro-investing and financial wellness app", "$507M", "Late", 2012, "Irvine, CA"),
        ]),
        sub("embedded-finance", "Embedded Finance & BaaS", [
            c("Plaid", "plaid.com", "Financial data connectivity infrastructure", "$734M", "Late", 2013, "San Francisco, CA"),
            c("Unit", "unit.co", "Banking-as-a-service API platform", "$189M", "Growth", 2019, "New York, NY"),
            c("Treasury Prime", "treasuryprime.com", "BaaS platform connecting banks and fintechs", "$78M", "Growth", 2017, "San Francisco, CA"),
            c("Synctera", "synctera.com", "Banking-as-a-service for fintech companies", "$94M", "Growth", 2020, "San Francisco, CA"),
            c("Alloy", "alloy.com", "Identity decisioning platform for financial services", "$187M", "Growth", 2015, "New York, NY"),
            c("Sardine", "sardine.ai", "Fraud prevention and compliance platform", "$75M", "Growth", 2020, "San Francisco, CA"),
        ]),
        sub("crypto-digital-assets", "Crypto & Digital Assets", [
            c("Coinbase", "coinbase.com", "Largest US cryptocurrency exchange", "Public", "Public", 2012, "Remote (US)"),
            c("Chainalysis", "chainalysis.com", "Blockchain analytics and compliance", "$536M", "Late", 2014, "New York, NY"),
            c("Fireblocks", "fireblocks.com", "Digital asset custody and transfer platform", "$1B", "Late", 2018, "New York, NY"),
            c("Circle", "circle.com", "Issuer of USDC stablecoin", "$1.1B", "Late", 2013, "Boston, MA"),
            c("Paxos", "paxos.com", "Regulated blockchain infrastructure", "$541M", "Late", 2012, "New York, NY"),
            c("Anchorage Digital", "anchorage.com", "Institutional digital asset platform", "$487M", "Late", 2017, "San Francisco, CA"),
        ]),
    ]),

    # ── 3. Healthcare & Biotech ──
    ind("healthcare-biotech", "Healthcare & Biotech", [
        sub("digital-health", "Digital Health & Telehealth", [
            c("Teladoc Health", "teladoc.com", "Virtual healthcare and telehealth platform", "Public", "Public", 2002, "Purchase, NY"),
            c("Hims & Hers", "hims.com", "Telehealth platform for wellness and personal care", "Public", "Public", 2017, "San Francisco, CA"),
            c("Ro", "ro.co", "Direct-to-patient telehealth and pharmacy", "$876M", "Late", 2017, "New York, NY"),
            c("Carbon Health", "carbonhealth.com", "Tech-enabled primary and urgent care", "$350M", "Growth", 2015, "San Francisco, CA"),
            c("Devoted Health", "devoted.com", "Medicare Advantage health plan for seniors", "$1.8B", "Late", 2017, "Waltham, MA"),
            c("Cityblock Health", "cityblock.com", "Value-based care for underserved communities", "$900M", "Late", 2017, "Brooklyn, NY"),
            c("Aledade", "aledade.com", "Value-based primary care network", "$303M", "Growth", 2014, "Bethesda, MD"),
        ]),
        sub("drug-discovery", "Drug Discovery & Pharma Tech", [
            c("Recursion", "recursionpharma.com", "AI-driven drug discovery platform", "Public", "Public", 2013, "Salt Lake City, UT"),
            c("Insitro", "insitro.com", "Machine learning for drug discovery", "$643M", "Late", 2018, "South San Francisco, CA"),
            c("Insilico Medicine", "insilico.com", "AI platform for drug discovery and development", "$407M", "Growth", 2014, "New York, NY"),
            c("Relay Therapeutics", "relaytx.com", "Motion-based drug design using AI", "Public", "Public", 2016, "Cambridge, MA"),
            c("Exscientia", "exscientia.ai", "AI-driven pharma tech for precision medicine", "Public", "Public", 2012, "Oxford, UK"),
            c("BenevolentAI", "benevolent.ai", "AI platform for scientific discovery", "Public", "Public", 2013, "London, UK"),
        ]),
        sub("medical-devices", "Medical Devices & MedTech", [
            c("Outset Medical", "outsetmedical.com", "Dialysis technology innovation", "Public", "Public", 2003, "San Jose, CA"),
            c("Butterfly Network", "butterflynetwork.com", "Handheld whole-body ultrasound device", "Public", "Public", 2011, "Burlington, MA"),
            c("Viz.ai", "viz.ai", "AI-powered clinical decision support for stroke care", "$252M", "Growth", 2016, "San Francisco, CA"),
            c("Aidoc", "aidoc.com", "AI radiology platform for medical imaging", "$250M", "Growth", 2016, "Tel Aviv, Israel"),
            c("Caption Health", "captionhealth.com", "AI-guided ultrasound imaging", "$53M", "Growth", 2013, "Brisbane, CA"),
            c("RapidAI", "rapidai.com", "AI platform for stroke and vascular care", "$25M", "Growth", 2012, "San Mateo, CA"),
        ]),
        sub("health-data", "Health Data & Analytics", [
            c("Veeva Systems", "veeva.com", "Cloud software for life sciences industry", "Public", "Public", 2007, "Pleasanton, CA"),
            c("Flatiron Health", "flatiron.com", "Oncology data and analytics platform", "$313M", "Late", 2012, "New York, NY"),
            c("Tempus", "tempus.com", "AI platform for precision medicine data", "$1.3B", "Late", 2015, "Chicago, IL"),
            c("Komodo Health", "komodohealth.com", "Healthcare data and analytics platform", "$434M", "Late", 2014, "San Francisco, CA"),
            c("Datavant", "datavant.com", "Health data connectivity and de-identification", "$343M", "Late", 2017, "San Francisco, CA"),
            c("Truveta", "truveta.com", "Health system data platform for research", "$295M", "Growth", 2020, "Seattle, WA"),
        ]),
        sub("mental-health", "Mental Health Tech", [
            c("Lyra Health", "lyrahealth.com", "Enterprise mental health benefits platform", "$910M", "Late", 2015, "Burlingame, CA"),
            c("Spring Health", "springhealth.com", "AI-powered mental health for employers", "$371M", "Growth", 2016, "New York, NY"),
            c("Headspace", "headspace.com", "Meditation and mindfulness app", "$431M", "Late", 2010, "Santa Monica, CA"),
            c("Talkspace", "talkspace.com", "Online therapy and counseling platform", "Public", "Public", 2012, "New York, NY"),
            c("Cerebral", "cerebral.com", "Online mental health treatment platform", "$300M", "Growth", 2020, "San Francisco, CA"),
            c("Calm", "calm.com", "Mental wellness and sleep app", "$218M", "Late", 2012, "San Francisco, CA"),
        ]),
        sub("genomics", "Genomics & Precision Medicine", [
            c("23andMe", "23andme.com", "Consumer genetics and precision health", "Public", "Public", 2006, "Sunnyvale, CA"),
            c("Illumina", "illumina.com", "Gene sequencing technology leader", "Public", "Public", 1998, "San Diego, CA"),
            c("10x Genomics", "10xgenomics.com", "Single-cell and spatial genomics instruments", "Public", "Public", 2012, "Pleasanton, CA"),
            c("Ginkgo Bioworks", "ginkgobioworks.com", "Synthetic biology platform for cell programming", "Public", "Public", 2008, "Boston, MA"),
            c("Sema4", "sema4.com", "Genomic-based clinical intelligence", "$782M", "Late", 2017, "Stamford, CT"),
            c("Color Health", "color.com", "Population health genomics platform", "$278M", "Growth", 2013, "Burlingame, CA"),
        ]),
    ]),

    # ── 4. Cybersecurity ──
    ind("cybersecurity", "Cybersecurity", [
        sub("cloud-security", "Cloud Security", [
            c("Wiz", "wiz.io", "Cloud security posture management platform", "$1.9B", "Late", 2020, "New York, NY"),
            c("Lacework", "lacework.com", "Cloud-native security and compliance", "$1.3B", "Late", 2015, "Mountain View, CA"),
            c("Orca Security", "orca.security", "Agentless cloud security platform", "$632M", "Late", 2019, "Portland, OR"),
            c("Aqua Security", "aquasec.com", "Cloud-native and container security", "$265M", "Growth", 2015, "Ramat Gan, Israel"),
            c("Sysdig", "sysdig.com", "Container and cloud security platform", "$774M", "Late", 2013, "San Francisco, CA"),
            c("Netskope", "netskope.com", "SASE and cloud security platform", "$1B", "Late", 2012, "Santa Clara, CA"),
        ]),
        sub("identity-access", "Identity & Access Management", [
            c("Okta", "okta.com", "Cloud identity and access management", "Public", "Public", 2009, "San Francisco, CA"),
            c("ForgeRock", "forgerock.com", "Enterprise identity management platform", "Public", "Public", 2010, "San Francisco, CA"),
            c("1Password", "1password.com", "Password management for individuals and teams", "$920M", "Late", 2005, "Toronto, Canada"),
            c("Transmit Security", "transmitsecurity.com", "Passwordless authentication and identity", "$543M", "Late", 2014, "Boston, MA"),
            c("Stytch", "stytch.com", "Developer-first authentication infrastructure", "$125M", "Growth", 2020, "San Francisco, CA"),
            c("Silverfort", "silverfort.com", "Unified identity protection platform", "$116M", "Growth", 2016, "Tel Aviv, Israel"),
        ]),
        sub("endpoint-security", "Endpoint Security", [
            c("CrowdStrike", "crowdstrike.com", "Cloud-native endpoint protection platform", "Public", "Public", 2011, "Austin, TX"),
            c("SentinelOne", "sentinelone.com", "AI-powered endpoint security", "Public", "Public", 2013, "Mountain View, CA"),
            c("Cybereason", "cybereason.com", "Endpoint detection and response platform", "$769M", "Late", 2012, "San Diego, CA"),
            c("Tanium", "tanium.com", "Endpoint management and security platform", "$1.1B", "Late", 2007, "Kirkland, WA"),
            c("Deep Instinct", "deepinstinct.com", "Deep learning for endpoint cybersecurity", "$321M", "Growth", 2015, "New York, NY"),
        ]),
        sub("appsec", "Application Security", [
            c("Snyk", "snyk.io", "Developer security for code and open source", "$1.4B", "Late", 2015, "Boston, MA"),
            c("Veracode", "veracode.com", "Application security testing platform", "$300M", "Late", 2006, "Burlington, MA"),
            c("Checkmarx", "checkmarx.com", "Application security testing solutions", "$550M", "Late", 2006, "Ramat Gan, Israel"),
            c("Apiiro", "apiiro.com", "Application risk management platform", "$175M", "Growth", 2019, "Tel Aviv, Israel"),
            c("Semgrep", "semgrep.dev", "Open-source static analysis for code security", "$100M", "Growth", 2017, "San Francisco, CA"),
            c("Legit Security", "legitsecurity.com", "Software supply chain security platform", "$77M", "Growth", 2020, "Palo Alto, CA"),
        ]),
        sub("threat-detection", "Threat Detection & Response", [
            c("Palo Alto Networks", "paloaltonetworks.com", "Network security and threat prevention", "Public", "Public", 2005, "Santa Clara, CA"),
            c("Splunk", "splunk.com", "Security analytics and SIEM platform", "Public", "Public", 2003, "San Francisco, CA"),
            c("Exabeam", "exabeam.com", "Next-gen SIEM and security analytics", "$390M", "Late", 2013, "Foster City, CA"),
            c("Hunters", "hunters.security", "SOC platform for threat detection", "$118M", "Growth", 2018, "Tel Aviv, Israel"),
            c("Recorded Future", "recordedfuture.com", "Threat intelligence platform", "$324M", "Late", 2009, "Boston, MA"),
            c("Securonix", "securonix.com", "Cloud-native SIEM and UEBA platform", "$1B", "Late", 2008, "Addison, TX"),
        ]),
        sub("data-privacy", "Data Privacy & Compliance", [
            c("OneTrust", "onetrust.com", "Privacy management and compliance platform", "$920M", "Late", 2016, "Atlanta, GA"),
            c("BigID", "bigid.com", "Data intelligence for privacy and protection", "$246M", "Growth", 2016, "New York, NY"),
            c("Drata", "drata.com", "Continuous compliance automation platform", "$328M", "Growth", 2020, "San Diego, CA"),
            c("Vanta", "vanta.com", "Automated security and compliance", "$203M", "Growth", 2018, "San Francisco, CA"),
            c("Securiti", "securiti.ai", "Data governance and privacy automation", "$231M", "Growth", 2018, "San Jose, CA"),
            c("TrustArc", "trustarc.com", "Privacy compliance management platform", "$70M", "Growth", 2001, "San Francisco, CA"),
        ]),
    ]),

    # ── 5. Enterprise SaaS ──
    ind("enterprise-saas", "Enterprise SaaS", [
        sub("crm-sales", "CRM & Sales Tech", [
            c("Salesforce", "salesforce.com", "World's leading CRM platform", "Public", "Public", 1999, "San Francisco, CA"),
            c("HubSpot", "hubspot.com", "Inbound marketing, sales, and CRM platform", "Public", "Public", 2006, "Cambridge, MA"),
            c("Gong", "gong.io", "Revenue intelligence and conversation analytics", "$584M", "Late", 2015, "San Francisco, CA"),
            c("Outreach", "outreach.io", "Sales engagement and execution platform", "$489M", "Late", 2014, "Seattle, WA"),
            c("Clari", "clari.com", "Revenue operations and forecasting platform", "$496M", "Late", 2012, "Sunnyvale, CA"),
            c("Apollo.io", "apollo.io", "Sales intelligence and engagement platform", "$251M", "Growth", 2015, "San Francisco, CA"),
            c("ZoomInfo", "zoominfo.com", "B2B data and go-to-market intelligence", "Public", "Public", 2000, "Vancouver, WA"),
        ]),
        sub("collaboration", "Collaboration & Productivity", [
            c("Notion", "notion.so", "All-in-one workspace for notes and collaboration", "$343M", "Late", 2013, "San Francisco, CA"),
            c("Figma", "figma.com", "Collaborative interface design platform", "$333M", "Late", 2012, "San Francisco, CA"),
            c("Miro", "miro.com", "Visual collaboration and whiteboarding platform", "$476M", "Late", 2011, "San Francisco, CA"),
            c("Airtable", "airtable.com", "Low-code platform for building apps", "$1.4B", "Late", 2012, "San Francisco, CA"),
            c("ClickUp", "clickup.com", "All-in-one productivity and project management", "$537M", "Late", 2017, "San Diego, CA"),
            c("Loom", "loom.com", "Async video messaging for work", "$200M", "Late", 2015, "San Francisco, CA"),
            c("Canva", "canva.com", "Online graphic design platform for everyone", "$572M", "Late", 2012, "Sydney, Australia"),
        ]),
        sub("data-analytics", "Data Analytics & BI", [
            c("Snowflake", "snowflake.com", "Cloud data warehousing platform", "Public", "Public", 2012, "Bozeman, MT"),
            c("Fivetran", "fivetran.com", "Automated data integration and ETL", "$730M", "Late", 2012, "Oakland, CA"),
            c("dbt Labs", "getdbt.com", "Data transformation framework and tools", "$414M", "Late", 2016, "Philadelphia, PA"),
            c("Hex", "hex.tech", "Collaborative data science and analytics", "$80M", "Growth", 2019, "San Francisco, CA"),
            c("Monte Carlo", "montecarlodata.com", "Data observability and reliability platform", "$236M", "Growth", 2019, "San Francisco, CA"),
            c("ThoughtSpot", "thoughtspot.com", "AI-powered analytics and search platform", "$744M", "Late", 2012, "Sunnyvale, CA"),
        ]),
        sub("devops-devtools", "DevOps & Developer Tools", [
            c("GitLab", "gitlab.com", "Complete DevOps platform in a single app", "Public", "Public", 2011, "Remote (US)"),
            c("HashiCorp", "hashicorp.com", "Cloud infrastructure automation tools", "Public", "Public", 2012, "San Francisco, CA"),
            c("Vercel", "vercel.com", "Frontend cloud platform for web development", "$313M", "Late", 2015, "San Francisco, CA"),
            c("Postman", "postman.com", "API development and collaboration platform", "$433M", "Late", 2014, "San Francisco, CA"),
            c("LaunchDarkly", "launchdarkly.com", "Feature management and experimentation platform", "$330M", "Late", 2014, "Oakland, CA"),
            c("Harness", "harness.io", "Modern software delivery and CI/CD platform", "$425M", "Late", 2016, "San Francisco, CA"),
            c("Fly.io", "fly.io", "Global application deployment platform", "$85M", "Growth", 2017, "Chicago, IL"),
        ]),
        sub("erp-backoffice", "ERP & Back Office", [
            c("ServiceNow", "servicenow.com", "Enterprise digital workflow platform", "Public", "Public", 2004, "Santa Clara, CA"),
            c("Workday", "workday.com", "Cloud ERP for finance and human resources", "Public", "Public", 2005, "Pleasanton, CA"),
            c("Ramp", "ramp.com", "Corporate card and spend management platform", "$1.6B", "Late", 2019, "New York, NY"),
            c("Brex", "brex.com", "Corporate cards and financial stack for startups", "$1.2B", "Late", 2017, "San Francisco, CA"),
            c("Navan", "navan.com", "Travel and expense management platform", "$1.5B", "Late", 2015, "Palo Alto, CA"),
            c("Tipalti", "tipalti.com", "Accounts payable and payment automation", "$550M", "Late", 2010, "Foster City, CA"),
        ]),
    ]),

    # ── 6. E-commerce & Retail Tech ──
    ind("ecommerce-retail", "E-commerce & Retail Tech", [
        sub("marketplaces", "Marketplaces", [
            c("Shopify", "shopify.com", "E-commerce platform for online stores", "Public", "Public", 2006, "Ottawa, Canada"),
            c("Faire", "faire.com", "Wholesale marketplace for independent retailers", "$1.3B", "Late", 2017, "San Francisco, CA"),
            c("Whatnot", "whatnot.com", "Live shopping marketplace platform", "$484M", "Late", 2019, "Marina del Rey, CA"),
            c("Temu", "temu.com", "Budget e-commerce marketplace", "Subsidiary", "Late", 2022, "Boston, MA"),
            c("StockX", "stockx.com", "Marketplace for sneakers and collectibles", "$690M", "Late", 2015, "Detroit, MI"),
            c("Poshmark", "poshmark.com", "Social commerce for fashion resale", "Public", "Public", 2011, "Redwood City, CA"),
        ]),
        sub("d2c-brand", "D2C & Brand Enablement", [
            c("BigCommerce", "bigcommerce.com", "Open SaaS e-commerce platform", "Public", "Public", 2009, "Austin, TX"),
            c("Attentive", "attentive.com", "SMS and email marketing for e-commerce", "$863M", "Late", 2016, "New York, NY"),
            c("Klaviyo", "klaviyo.com", "Marketing automation for e-commerce brands", "Public", "Public", 2012, "Boston, MA"),
            c("Yotpo", "yotpo.com", "E-commerce marketing platform for reviews", "$416M", "Late", 2011, "New York, NY"),
            c("Gorgias", "gorgias.com", "E-commerce customer support helpdesk", "$71M", "Growth", 2015, "San Francisco, CA"),
            c("Triple Whale", "triplewhale.com", "E-commerce analytics and attribution", "$52M", "Growth", 2021, "Columbus, OH"),
        ]),
        sub("retail-analytics", "Retail Analytics & Operations", [
            c("Celect", "celect.com", "AI-driven inventory optimization for retail", "$30M", "Growth", 2013, "Boston, MA"),
            c("SymphonyAI", "symphonyai.com", "AI for retail and CPG analytics", "$60M", "Growth", 2017, "Palo Alto, CA"),
            c("Trax", "traxretail.com", "Computer vision for retail shelf analytics", "$640M", "Late", 2010, "Singapore"),
            c("Crisp", "gocrisp.com", "Retail data platform for CPG brands", "$50M", "Growth", 2016, "New York, NY"),
            c("Shelf Engine", "shelfengine.com", "AI for automated grocery ordering", "$57M", "Growth", 2016, "Seattle, WA"),
        ]),
        sub("social-commerce", "Social Commerce", [
            c("LTK", "shopltk.com", "Creator-driven shopping platform", "$300M", "Late", 2011, "Dallas, TX"),
            c("Flip", "flip.shop", "Social commerce for beauty product reviews", "$95M", "Growth", 2019, "Los Angeles, CA"),
            c("Verishop", "verishop.com", "Social shopping for premium brands", "$40M", "Growth", 2019, "Los Angeles, CA"),
            c("ShopMy", "shopmy.us", "Creator commerce and affiliate platform", "$28M", "Early", 2020, "New York, NY"),
            c("Supergreat", "supergreat.com", "Video-first beauty commerce platform", "$10M", "Early", 2018, "New York, NY"),
        ]),
        sub("commerce-infra", "Commerce Infrastructure", [
            c("Bolt", "bolt.com", "One-click checkout infrastructure", "$998M", "Late", 2014, "San Francisco, CA"),
            c("Ordergroove", "ordergroove.com", "Subscription commerce platform for brands", "$100M", "Growth", 2010, "New York, NY"),
            c("Shippo", "goshippo.com", "Multi-carrier shipping API for e-commerce", "$110M", "Growth", 2013, "San Francisco, CA"),
            c("ShipBob", "shipbob.com", "E-commerce fulfillment and logistics platform", "$330M", "Late", 2014, "Chicago, IL"),
            c("Recharge", "rechargepayments.com", "Subscription management for e-commerce", "$277M", "Late", 2014, "Santa Monica, CA"),
            c("Narvar", "narvar.com", "Post-purchase customer experience platform", "$64M", "Growth", 2012, "San Francisco, CA"),
        ]),
    ]),

    # ── 7. Climate Tech & Clean Energy ──
    ind("climate-cleanenergy", "Climate Tech & Clean Energy", [
        sub("solar-wind", "Solar & Wind Energy", [
            c("Enphase Energy", "enphase.com", "Solar microinverters and energy systems", "Public", "Public", 2006, "Fremont, CA"),
            c("Sunrun", "sunrun.com", "Residential solar energy provider", "Public", "Public", 2007, "San Francisco, CA"),
            c("Aurora Solar", "aurorasolar.com", "Solar design and sales software platform", "$420M", "Late", 2013, "San Francisco, CA"),
            c("Palmetto", "palmetto.com", "Clean energy marketplace for homeowners", "$391M", "Growth", 2010, "Charleston, SC"),
            c("Arcadia", "arcadia.com", "Clean energy access platform for consumers", "$200M", "Growth", 2014, "Washington, DC"),
        ]),
        sub("energy-storage", "Energy Storage & Batteries", [
            c("QuantumScape", "quantumscape.com", "Solid-state lithium-metal battery developer", "Public", "Public", 2010, "San Jose, CA"),
            c("Form Energy", "formenergy.com", "Long-duration iron-air batteries for grid storage", "$807M", "Late", 2017, "Somerville, MA"),
            c("EnerVenue", "enervenue.com", "Metal-hydrogen battery technology", "$368M", "Growth", 2020, "Fremont, CA"),
            c("Sila Nanotechnologies", "silanano.com", "Next-gen silicon anode battery materials", "$930M", "Late", 2011, "Alameda, CA"),
            c("Eos Energy", "eose.com", "Zinc-based long-duration energy storage", "Public", "Public", 2008, "Edison, NJ"),
            c("ESS Inc", "essinc.com", "Iron flow battery for long-duration storage", "Public", "Public", 2011, "Wilsonville, OR"),
        ]),
        sub("carbon-capture", "Carbon Capture & Removal", [
            c("Climeworks", "climeworks.com", "Direct air capture of carbon dioxide", "$780M", "Late", 2009, "Zurich, Switzerland"),
            c("Heirloom", "heirloomcarbon.com", "Direct air capture using limestone", "$153M", "Growth", 2020, "San Francisco, CA"),
            c("Charm Industrial", "charmindustrial.com", "Bio-oil carbon removal technology", "$100M", "Growth", 2018, "San Francisco, CA"),
            c("CarbonCure", "carboncure.com", "Carbon mineralization in concrete", "$106M", "Growth", 2007, "Dartmouth, Canada"),
            c("Running Tide", "runningtide.com", "Ocean-based carbon removal solutions", "$54M", "Growth", 2017, "Portland, ME"),
        ]),
        sub("ev-infra", "EV & Electric Mobility", [
            c("Rivian", "rivian.com", "Electric adventure vehicles manufacturer", "Public", "Public", 2009, "Irvine, CA"),
            c("Lucid Motors", "lucidmotors.com", "Luxury electric vehicle manufacturer", "Public", "Public", 2007, "Newark, CA"),
            c("ChargePoint", "chargepoint.com", "Electric vehicle charging network", "Public", "Public", 2007, "Campbell, CA"),
            c("Electrify America", "electrifyamerica.com", "High-speed EV charging network", "Subsidiary", "Late", 2017, "Reston, VA"),
            c("EVgo", "evgo.com", "Public fast charging network for EVs", "Public", "Public", 2010, "Los Angeles, CA"),
            c("Wallbox", "wallbox.com", "Smart EV charging and energy management", "Public", "Public", 2015, "Barcelona, Spain"),
        ]),
        sub("grid-energy", "Grid & Energy Management", [
            c("Arcadia", "arcadia.com", "Clean energy data and management platform", "$200M", "Growth", 2014, "Washington, DC"),
            c("Stem Inc", "stem.com", "AI-driven energy storage optimization", "Public", "Public", 2009, "San Francisco, CA"),
            c("Utilidata", "utilidata.com", "AI-powered grid edge software", "$78M", "Growth", 2012, "Providence, RI"),
            c("GridBeyond", "gridbeyond.com", "Intelligent energy management platform", "$52M", "Growth", 2007, "Dublin, Ireland"),
            c("AutoGrid", "auto-grid.com", "AI for distributed energy resource management", "$71M", "Growth", 2011, "Redwood City, CA"),
        ]),
        sub("sustainable-materials", "Sustainable Materials & Circular Economy", [
            c("Bolt Threads", "boltthreads.com", "Bio-based materials and sustainable textiles", "$313M", "Late", 2009, "Emeryville, CA"),
            c("Solugen", "solugen.com", "Bio-based chemicals from plant sugars", "$435M", "Growth", 2016, "Houston, TX"),
            c("Novamont", "novamont.com", "Biodegradable and compostable bioplastics", "$100M", "Late", 1989, "Novara, Italy"),
            c("Twelve", "twelve.co", "CO2 to chemicals transformation technology", "$200M", "Growth", 2015, "Berkeley, CA"),
            c("LanzaTech", "lanzatech.com", "Carbon recycling biotechnology platform", "Public", "Public", 2005, "Skokie, IL"),
        ]),
    ]),

    # ── 8. Real Estate & PropTech ──
    ind("real-estate-proptech", "Real Estate & PropTech", [
        sub("property-mgmt", "Property Management", [
            c("AppFolio", "appfolio.com", "Cloud property management software", "Public", "Public", 2006, "Santa Barbara, CA"),
            c("Buildium", "buildium.com", "Property management software for landlords", "$65M", "Late", 2004, "Boston, MA"),
            c("Latch", "latch.com", "Smart access and building management", "Public", "Public", 2014, "New York, NY"),
            c("Entrata", "entrata.com", "Property management and leasing software", "$507M", "Late", 2003, "Lehi, UT"),
            c("RealPage", "realpage.com", "Real estate management software and analytics", "$1.3B", "Late", 1998, "Richardson, TX"),
        ]),
        sub("re-marketplace", "Real Estate Marketplaces", [
            c("Opendoor", "opendoor.com", "Digital platform for buying and selling homes", "Public", "Public", 2014, "San Francisco, CA"),
            c("Offerpad", "offerpad.com", "Real estate iBuying platform", "Public", "Public", 2015, "Chandler, AZ"),
            c("Compass", "compass.com", "Technology-driven real estate brokerage", "Public", "Public", 2012, "New York, NY"),
            c("Redfin", "redfin.com", "Tech-powered real estate brokerage", "Public", "Public", 2004, "Seattle, WA"),
            c("Flyhomes", "flyhomes.com", "Cash-offer real estate platform", "$290M", "Growth", 2016, "Seattle, WA"),
        ]),
        sub("construction-tech", "Construction Tech", [
            c("Procore", "procore.com", "Cloud-based construction management platform", "Public", "Public", 2002, "Carpinteria, CA"),
            c("Built Technologies", "getbuilt.com", "Construction lending software", "$315M", "Late", 2014, "Nashville, TN"),
            c("Katerra", "katerra.com", "Tech-driven offsite construction", "$2B", "Late", 2015, "Menlo Park, CA"),
            c("PlanGrid", "plangrid.com", "Construction productivity software", "$99M", "Late", 2011, "San Francisco, CA"),
            c("Briq", "briq.com", "AI financial automation for construction", "$71M", "Growth", 2018, "Santa Barbara, CA"),
            c("OpenSpace", "openspace.ai", "AI-powered construction photo documentation", "$116M", "Growth", 2017, "San Francisco, CA"),
        ]),
        sub("mortgage-tech", "Mortgage & Lending Tech", [
            c("Better.com", "better.com", "Digital mortgage origination platform", "$905M", "Public", 2014, "New York, NY"),
            c("Blend", "blend.com", "Digital lending platform for banks", "Public", "Public", 2012, "San Francisco, CA"),
            c("Divvy Homes", "divvyhomes.com", "Rent-to-own homeownership platform", "$735M", "Late", 2017, "San Francisco, CA"),
            c("Arrived", "arrived.com", "Fractional real estate investment platform", "$162M", "Growth", 2019, "Seattle, WA"),
            c("Landis", "landis.com", "Path to homeownership for renters", "$165M", "Growth", 2019, "New York, NY"),
        ]),
        sub("smart-buildings", "Smart Buildings & IoT", [
            c("VTS", "vts.com", "Commercial real estate leasing platform", "$300M", "Late", 2012, "New York, NY"),
            c("Enertiv", "enertiv.com", "Building performance and IoT analytics", "$20M", "Early", 2012, "New York, NY"),
            c("Measurabl", "measurabl.com", "ESG data management for real estate", "$93M", "Growth", 2013, "San Diego, CA"),
            c("75F", "75f.io", "IoT smart building automation system", "$60M", "Growth", 2012, "Burnsville, MN"),
            c("Aquicore", "aquicore.com", "Real-time building energy management", "$25M", "Early", 2013, "Washington, DC"),
        ]),
    ]),

    # ── 9. Education Tech ──
    ind("edtech", "Education Tech", [
        sub("k12", "K-12 EdTech", [
            c("Newsela", "newsela.com", "Instructional content platform for K-12", "$188M", "Late", 2013, "New York, NY"),
            c("Paper", "paper.co", "AI-powered tutoring for school districts", "$271M", "Late", 2014, "Montreal, Canada"),
            c("GoGuardian", "goguardian.com", "Digital learning tools for K-12 schools", "$200M", "Late", 2014, "El Segundo, CA"),
            c("Clever", "clever.com", "Single sign-on and data platform for schools", "$55M", "Growth", 2012, "San Francisco, CA"),
            c("Kami", "kamiapp.com", "Document annotation tool for classrooms", "$30M", "Growth", 2013, "Auckland, New Zealand"),
        ]),
        sub("online-learning", "Online Learning Platforms", [
            c("Coursera", "coursera.org", "Online learning platform for higher education", "Public", "Public", 2012, "Mountain View, CA"),
            c("Udemy", "udemy.com", "Online course marketplace for skills", "Public", "Public", 2010, "San Francisco, CA"),
            c("Masterclass", "masterclass.com", "Premium online classes from world-class experts", "$461M", "Late", 2015, "San Francisco, CA"),
            c("Skillshare", "skillshare.com", "Online learning community for creatives", "$110M", "Late", 2010, "New York, NY"),
            c("Outlier.org", "outlier.org", "Online college courses for credit", "$30M", "Growth", 2019, "New York, NY"),
            c("Khan Academy", "khanacademy.org", "Free world-class education for anyone", "$30M", "Non-profit", 2008, "Mountain View, CA"),
        ]),
        sub("corporate-training", "Corporate Training & L&D", [
            c("Degreed", "degreed.com", "Workforce upskilling and learning platform", "$375M", "Late", 2012, "Pleasanton, CA"),
            c("Docebo", "docebo.com", "AI-powered enterprise learning platform", "Public", "Public", 2005, "Toronto, Canada"),
            c("360Learning", "360learning.com", "Collaborative corporate learning platform", "$241M", "Growth", 2013, "New York, NY"),
            c("Articulate", "articulate.com", "E-learning authoring tools for enterprises", "$1.5B", "Late", 2002, "New York, NY"),
            c("Cornerstone OnDemand", "cornerstoneondemand.com", "Talent management and learning software", "$1.3B", "Late", 1999, "Santa Monica, CA"),
        ]),
        sub("language-learning", "Language Learning", [
            c("Duolingo", "duolingo.com", "Gamified language learning app", "Public", "Public", 2011, "Pittsburgh, PA"),
            c("Babbel", "babbel.com", "Language learning subscription app", "$300M", "Late", 2007, "Berlin, Germany"),
            c("Busuu", "busuu.com", "Social language learning platform", "$30M", "Growth", 2008, "London, UK"),
            c("Preply", "preply.com", "Online language tutoring marketplace", "$100M", "Growth", 2012, "Barcelona, Spain"),
            c("EF Education First", "ef.com", "Global language and education company", "$500M", "Late", 1965, "Lucerne, Switzerland"),
        ]),
        sub("edtech-infra", "EdTech Infrastructure", [
            c("Instructure", "instructure.com", "Canvas learning management system", "$200M", "Late", 2008, "Salt Lake City, UT"),
            c("PowerSchool", "powerschool.com", "K-12 education technology platform", "Public", "Public", 1997, "Folsom, CA"),
            c("Anthology", "anthology.com", "Higher education SaaS platform", "$300M", "Late", 2003, "Boca Raton, FL"),
            c("ClassLink", "classlink.com", "Single sign-on and analytics for schools", "$50M", "Growth", 2009, "Clifton, NJ"),
            c("Turnitin", "turnitin.com", "Academic integrity and plagiarism detection", "$1.7B", "Late", 1998, "Oakland, CA"),
        ]),
    ]),

    # ── 10. Supply Chain & Logistics ──
    ind("supply-chain", "Supply Chain & Logistics", [
        sub("last-mile", "Last-Mile Delivery", [
            c("DoorDash", "doordash.com", "On-demand food and goods delivery", "Public", "Public", 2013, "San Francisco, CA"),
            c("Instacart", "instacart.com", "Grocery delivery and pickup platform", "Public", "Public", 2012, "San Francisco, CA"),
            c("Gopuff", "gopuff.com", "Instant delivery of essentials", "$3.4B", "Late", 2013, "Philadelphia, PA"),
            c("Bringg", "bringg.com", "Delivery and fulfillment orchestration platform", "$113M", "Growth", 2013, "Chicago, IL"),
            c("Veho", "shipveho.com", "Next-day package delivery service", "$246M", "Growth", 2020, "Boulder, CO"),
            c("Coco", "cocodelivery.com", "Autonomous sidewalk delivery robots", "$56M", "Growth", 2020, "Los Angeles, CA"),
        ]),
        sub("freight-trucking", "Freight & Trucking Tech", [
            c("Flexport", "flexport.com", "Tech-forward global freight forwarding", "$2.3B", "Late", 2013, "San Francisco, CA"),
            c("Convoy", "convoy.com", "Digital freight network for trucking", "$900M", "Late", 2015, "Seattle, WA"),
            c("Loadsmart", "loadsmart.com", "AI-powered freight management platform", "$276M", "Growth", 2014, "Chicago, IL"),
            c("Transfix", "transfix.io", "Digital freight marketplace", "$149M", "Growth", 2013, "New York, NY"),
            c("FourKites", "fourkites.com", "Real-time supply chain visibility platform", "$200M", "Growth", 2014, "Chicago, IL"),
            c("project44", "project44.com", "Advanced visibility platform for shippers", "$602M", "Late", 2014, "Chicago, IL"),
        ]),
        sub("warehouse-auto", "Warehouse & Fulfillment Automation", [
            c("Locus Robotics", "locusrobotics.com", "Autonomous mobile robots for warehouses", "$380M", "Late", 2014, "Wilmington, MA"),
            c("Berkshire Grey", "berkshiregrey.com", "AI-powered robotic picking and sorting", "Public", "Public", 2013, "Bedford, MA"),
            c("6 River Systems", "6river.com", "Collaborative mobile robots for fulfillment", "$46M", "Late", 2015, "Waltham, MA"),
            c("Fabric", "getfabric.com", "Micro-fulfillment center technology", "$326M", "Late", 2015, "Tel Aviv, Israel"),
            c("Attabotics", "attabotics.com", "3D robotic supply chain technology", "$110M", "Growth", 2016, "Calgary, Canada"),
        ]),
        sub("supply-visibility", "Supply Chain Visibility & Planning", [
            c("Kinaxis", "kinaxis.com", "Supply chain planning and management", "Public", "Public", 1984, "Ottawa, Canada"),
            c("o9 Solutions", "o9solutions.com", "AI-powered supply chain planning platform", "$295M", "Late", 2009, "Dallas, TX"),
            c("Coupa", "coupa.com", "Business spend management platform", "$1B", "Late", 2006, "San Mateo, CA"),
            c("E2open", "e2open.com", "Connected supply chain platform", "Public", "Public", 2000, "Austin, TX"),
            c("Anaplan", "anaplan.com", "Connected planning and business modeling", "$900M", "Late", 2006, "San Francisco, CA"),
        ]),
        sub("procurement", "Procurement & Sourcing", [
            c("Jaggaer", "jaggaer.com", "Procurement and spend management suite", "$300M", "Late", 1995, "Research Triangle Park, NC"),
            c("Zip", "ziphq.com", "Intake-to-procure orchestration platform", "$100M", "Growth", 2020, "San Francisco, CA"),
            c("Fairmarkit", "fairmarkit.com", "AI-driven autonomous sourcing", "$68M", "Growth", 2017, "Boston, MA"),
            c("Globality", "globality.com", "AI platform for strategic sourcing", "$205M", "Growth", 2015, "Menlo Park, CA"),
            c("Scoutbee", "scoutbee.com", "AI-powered supplier discovery platform", "$76M", "Growth", 2015, "Berlin, Germany"),
        ]),
    ]),

    # ── 11. Food & Agriculture ──
    ind("food-agriculture", "Food & Agriculture", [
        sub("agtech", "AgTech & Precision Agriculture", [
            c("Indigo Agriculture", "indigoag.com", "Microbiology and digital ag platform", "$1.2B", "Late", 2013, "Boston, MA"),
            c("Farmers Business Network", "fbn.com", "Data-driven farmer network and marketplace", "$918M", "Late", 2014, "San Carlos, CA"),
            c("Arable", "arable.com", "Crop intelligence and weather analytics", "$58M", "Growth", 2013, "San Francisco, CA"),
            c("Pivot Bio", "pivotbio.com", "Microbial nitrogen for crop nutrition", "$617M", "Late", 2011, "Berkeley, CA"),
            c("CropX", "cropx.com", "AI-driven soil sensing and farm management", "$30M", "Growth", 2015, "San Francisco, CA"),
        ]),
        sub("food-delivery", "Food Delivery & Ghost Kitchens", [
            c("DoorDash", "doordash.com", "On-demand food delivery platform", "Public", "Public", 2013, "San Francisco, CA"),
            c("Uber Eats", "ubereats.com", "Food delivery arm of Uber", "Public", "Public", 2014, "San Francisco, CA"),
            c("Kitchen United", "kitchenunited.com", "Multi-restaurant kitchen facilities", "$100M", "Growth", 2017, "Pasadena, CA"),
            c("CloudKitchens", "cloudkitchens.com", "Ghost kitchen real estate platform", "$850M", "Late", 2018, "Los Angeles, CA"),
            c("Reef Technology", "reeftechnology.com", "Proximity hub infrastructure for food and logistics", "$1.5B", "Late", 2013, "Miami, FL"),
        ]),
        sub("alt-protein", "Alternative Protein", [
            c("Impossible Foods", "impossiblefoods.com", "Plant-based meat alternatives", "$2B", "Late", 2011, "Redwood City, CA"),
            c("Beyond Meat", "beyondmeat.com", "Plant-based meat products", "Public", "Public", 2009, "El Segundo, CA"),
            c("Upside Foods", "upsidefoods.com", "Cultivated meat grown from animal cells", "$608M", "Late", 2015, "Berkeley, CA"),
            c("Perfect Day", "perfectday.com", "Animal-free dairy protein via fermentation", "$750M", "Late", 2014, "Berkeley, CA"),
            c("Eat Just", "ju.st", "Plant-based eggs and cultivated meat", "$800M", "Late", 2011, "San Francisco, CA"),
            c("NotCo", "notco.com", "AI-powered plant-based food company", "$431M", "Late", 2015, "Santiago, Chile"),
        ]),
        sub("restaurant-tech", "Restaurant Tech", [
            c("Toast", "toasttab.com", "Restaurant management and POS platform", "Public", "Public", 2012, "Boston, MA"),
            c("Olo", "olo.com", "Digital ordering platform for restaurants", "Public", "Public", 2005, "New York, NY"),
            c("SpotOn", "spoton.com", "Restaurant and SMB payment and software", "$893M", "Late", 2017, "San Francisco, CA"),
            c("MarginEdge", "marginedge.com", "Restaurant management and accounting software", "$45M", "Growth", 2015, "Fairfax, VA"),
            c("Incentivio", "incentivio.com", "Guest engagement platform for restaurants", "$20M", "Early", 2016, "Atlanta, GA"),
        ]),
        sub("grocery-commerce", "Grocery & Food Commerce", [
            c("Instacart", "instacart.com", "Grocery delivery and pickup platform", "Public", "Public", 2012, "San Francisco, CA"),
            c("Swiftly", "swiftly.com", "Retail technology platform for grocers", "$137M", "Growth", 2018, "Seattle, WA"),
            c("Flashfood", "flashfood.com", "Marketplace for discounted near-expiry food", "$36M", "Growth", 2016, "Toronto, Canada"),
            c("Misfits Market", "misfitsmarket.com", "Affordable grocery delivery service", "$526M", "Late", 2018, "Pennsauken, NJ"),
            c("Thrive Market", "thrivemarket.com", "Online organic grocery membership retailer", "$251M", "Late", 2014, "Los Angeles, CA"),
        ]),
    ]),

    # ── 12. Mobility & Transportation ──
    ind("mobility-transport", "Mobility & Transportation", [
        sub("ridehailing", "Ride-Hailing & Shared Mobility", [
            c("Uber", "uber.com", "Global ride-hailing and mobility platform", "Public", "Public", 2009, "San Francisco, CA"),
            c("Lyft", "lyft.com", "US ride-hailing and transportation", "Public", "Public", 2012, "San Francisco, CA"),
            c("Grab", "grab.com", "Southeast Asian super app for mobility", "Public", "Public", 2012, "Singapore"),
            c("BlaBlaCar", "blablacar.com", "Long-distance carpooling platform", "$450M", "Late", 2006, "Paris, France"),
            c("Via", "ridewithvia.com", "Shared ride and transit technology platform", "$568M", "Late", 2012, "New York, NY"),
        ]),
        sub("autonomous-vehicles", "Autonomous Vehicles", [
            c("Waymo", "waymo.com", "Google's autonomous driving technology company", "Subsidiary", "Late", 2009, "Mountain View, CA"),
            c("Cruise", "getcruise.com", "GM-backed autonomous vehicle company", "$10B", "Late", 2013, "San Francisco, CA"),
            c("Aurora Innovation", "aurora.tech", "Self-driving technology for trucks and cars", "Public", "Public", 2017, "Pittsburgh, PA"),
            c("Nuro", "nuro.ai", "Autonomous delivery vehicles", "$2.1B", "Late", 2016, "Mountain View, CA"),
            c("Motional", "motional.com", "Hyundai-Aptiv autonomous driving JV", "$4B", "Late", 2020, "Boston, MA"),
            c("Pony.ai", "pony.ai", "Autonomous driving technology company", "$1.3B", "Late", 2016, "Fremont, CA"),
        ]),
        sub("electric-vehicles", "Electric Vehicles", [
            c("Tesla", "tesla.com", "Electric vehicles and clean energy", "Public", "Public", 2003, "Austin, TX"),
            c("Rivian", "rivian.com", "Electric adventure vehicles and delivery vans", "Public", "Public", 2009, "Irvine, CA"),
            c("Lucid Motors", "lucidmotors.com", "Luxury electric sedan manufacturer", "Public", "Public", 2007, "Newark, CA"),
            c("Fisker", "fiskerinc.com", "Affordable electric vehicle manufacturer", "Public", "Public", 2016, "Manhattan Beach, CA"),
            c("VinFast", "vinfast.com", "Vietnamese electric vehicle manufacturer", "Public", "Public", 2017, "Haiphong, Vietnam"),
            c("Canoo", "canoo.com", "Lifestyle electric vehicles", "Public", "Public", 2017, "Justin, TX"),
        ]),
        sub("micromobility", "Micro-Mobility", [
            c("Lime", "li.me", "Electric scooter and bike sharing", "$977M", "Late", 2017, "San Francisco, CA"),
            c("Bird", "bird.co", "Electric scooter sharing platform", "$758M", "Late", 2017, "Miami, FL"),
            c("Tier Mobility", "tier.app", "European micro-mobility platform", "$660M", "Late", 2018, "Berlin, Germany"),
            c("Voi Technology", "voiscooters.com", "European e-scooter sharing service", "$400M", "Growth", 2018, "Stockholm, Sweden"),
            c("Superpedestrian", "superpedestrian.com", "E-scooter fleet with vehicle intelligence", "$175M", "Growth", 2013, "Cambridge, MA"),
        ]),
        sub("fleet-mgmt", "Fleet Management", [
            c("Samsara", "samsara.com", "IoT platform for fleet and operations", "Public", "Public", 2015, "San Francisco, CA"),
            c("Motive", "gomotive.com", "Fleet management and safety platform", "$600M", "Late", 2013, "San Francisco, CA"),
            c("Geotab", "geotab.com", "Telematics and fleet management platform", "$165M", "Late", 2000, "Oakville, Canada"),
            c("Platform Science", "platformscience.com", "Open IoT platform for trucking fleets", "$340M", "Late", 2015, "San Diego, CA"),
            c("ClearPathGPS", "clearpathgps.com", "GPS fleet tracking and management", "$20M", "Growth", 2013, "San Diego, CA"),
        ]),
    ]),

    # ── 13. Media & Entertainment ──
    ind("media-entertainment", "Media & Entertainment", [
        sub("streaming-content", "Streaming & Content", [
            c("Spotify", "spotify.com", "Music and podcast streaming platform", "Public", "Public", 2006, "Stockholm, Sweden"),
            c("Roku", "roku.com", "Streaming platform and devices", "Public", "Public", 2002, "San Jose, CA"),
            c("Crunchyroll", "crunchyroll.com", "Anime streaming and media platform", "Subsidiary", "Late", 2006, "San Francisco, CA"),
            c("Vimeo", "vimeo.com", "Professional video hosting and tools", "Public", "Public", 2004, "New York, NY"),
            c("Plex", "plex.tv", "Personal media streaming platform", "$115M", "Growth", 2009, "Los Gatos, CA"),
        ]),
        sub("gaming", "Gaming", [
            c("Epic Games", "epicgames.com", "Fortnite and Unreal Engine developer", "$5.4B", "Late", 1991, "Cary, NC"),
            c("Roblox", "roblox.com", "Social gaming platform and creation engine", "Public", "Public", 2004, "San Mateo, CA"),
            c("Unity Technologies", "unity.com", "Real-time 3D game development platform", "Public", "Public", 2004, "San Francisco, CA"),
            c("Discord", "discord.com", "Voice, video, and text chat for communities", "$982M", "Late", 2012, "San Francisco, CA"),
            c("Overwolf", "overwolf.com", "In-game creation platform for mods and apps", "$145M", "Growth", 2010, "Tel Aviv, Israel"),
        ]),
        sub("creator-economy", "Creator Economy", [
            c("Patreon", "patreon.com", "Membership platform for content creators", "$412M", "Late", 2013, "San Francisco, CA"),
            c("Substack", "substack.com", "Newsletter publishing and subscription platform", "$82M", "Growth", 2017, "San Francisco, CA"),
            c("Cameo", "cameo.com", "Personalized celebrity video platform", "$166M", "Late", 2017, "Chicago, IL"),
            c("Spring", "spri.ng", "Creator commerce and merchandise platform", "$69M", "Growth", 2012, "Louisville, KY"),
            c("Beacons", "beacons.ai", "AI-powered link-in-bio and creator toolkit", "$33M", "Growth", 2020, "San Francisco, CA"),
            c("Stan", "stan.store", "All-in-one creator storefront and link-in-bio", "$12M", "Early", 2021, "San Francisco, CA"),
        ]),
        sub("adtech", "Advertising Tech", [
            c("The Trade Desk", "thetradedesk.com", "Programmatic advertising platform", "Public", "Public", 2009, "Ventura, CA"),
            c("IAS", "integralads.com", "Digital ad verification and optimization", "Public", "Public", 2009, "New York, NY"),
            c("DoubleVerify", "doubleverify.com", "Digital media measurement and analytics", "Public", "Public", 2008, "New York, NY"),
            c("LiveRamp", "liveramp.com", "Data connectivity for marketing", "Public", "Public", 2011, "San Francisco, CA"),
            c("Moloco", "moloco.com", "Machine learning ad tech platform", "$198M", "Growth", 2013, "Redwood City, CA"),
        ]),
        sub("sports-tech", "Sports Tech", [
            c("Sportradar", "sportradar.com", "Sports data and content platform", "Public", "Public", 2001, "St. Gallen, Switzerland"),
            c("Genius Sports", "geniussports.com", "Sports data technology provider", "Public", "Public", 2001, "London, UK"),
            c("Catapult Sports", "catapultsports.com", "Athlete performance analytics technology", "Public", "Public", 2006, "Melbourne, Australia"),
            c("Overtime", "overtime.tv", "Sports media company for next gen fans", "$241M", "Growth", 2016, "New York, NY"),
            c("StatusPRO", "statusproent.com", "VR sports training and gaming", "$27M", "Early", 2018, "Nashville, TN"),
        ]),
    ]),

    # ── 14. Aerospace & Defense ──
    ind("aerospace-defense", "Aerospace & Defense", [
        sub("space-tech", "Space Tech & Satellites", [
            c("SpaceX", "spacex.com", "Rockets, satellites, and space transportation", "$9.4B", "Late", 2002, "Hawthorne, CA"),
            c("Rocket Lab", "rocketlabusa.com", "Small satellite launch and space systems", "Public", "Public", 2006, "Long Beach, CA"),
            c("Planet Labs", "planet.com", "Earth imaging satellite constellation", "Public", "Public", 2010, "San Francisco, CA"),
            c("Relativity Space", "relativityspace.com", "3D-printed rockets and space manufacturing", "$1.3B", "Late", 2015, "Long Beach, CA"),
            c("Astra", "astra.com", "Orbital launch services for small satellites", "Public", "Public", 2016, "Alameda, CA"),
            c("Spire Global", "spire.com", "Space-based data and analytics platform", "Public", "Public", 2012, "Vienna, VA"),
        ]),
        sub("defense-software", "Defense Software & AI", [
            c("Palantir", "palantir.com", "Data analytics for defense and intelligence", "Public", "Public", 2003, "Denver, CO"),
            c("Anduril", "anduril.com", "AI-powered defense technology platform", "$2.8B", "Late", 2017, "Costa Mesa, CA"),
            c("Shield AI", "shield.ai", "AI pilot for autonomous military aircraft", "$740M", "Late", 2015, "San Diego, CA"),
            c("Rebellion Defense", "rebelliondefense.com", "AI software for national security", "$150M", "Growth", 2019, "Washington, DC"),
            c("Second Front Systems", "secondfront.com", "Software-as-a-service for defense", "$72M", "Growth", 2019, "Arlington, VA"),
        ]),
        sub("drones-uav", "Drones & UAVs", [
            c("Skydio", "skydio.com", "Autonomous drone technology", "$660M", "Late", 2014, "San Mateo, CA"),
            c("Joby Aviation", "jobyaviation.com", "Electric air taxi and eVTOL aircraft", "Public", "Public", 2009, "Santa Cruz, CA"),
            c("Zipline", "flyzipline.com", "Autonomous drone delivery for medical supplies", "$583M", "Late", 2014, "South San Francisco, CA"),
            c("Archer Aviation", "archer.com", "Urban air mobility eVTOL aircraft", "Public", "Public", 2018, "San Jose, CA"),
            c("Wisk Aero", "wisk.aero", "Autonomous electric air taxi", "$450M", "Late", 2019, "Mountain View, CA"),
        ]),
        sub("aviation-tech", "Aviation Technology", [
            c("Boom Supersonic", "boomsupersonic.com", "Supersonic commercial aircraft", "$706M", "Late", 2014, "Centennial, CO"),
            c("Reliable Robotics", "reliable.co", "Remote piloting for cargo aircraft", "$133M", "Growth", 2017, "Mountain View, CA"),
            c("Merlin Labs", "merlinlabs.com", "Autonomous flight systems for aviation", "$105M", "Growth", 2018, "Boston, MA"),
            c("xwing", "xwing.com", "Autonomous flight technology for aviation", "$100M", "Growth", 2016, "San Francisco, CA"),
            c("Hermeus", "hermeus.com", "Hypersonic aircraft development", "$149M", "Growth", 2018, "Atlanta, GA"),
        ]),
        sub("geospatial", "Geospatial & Earth Observation", [
            c("Maxar Technologies", "maxar.com", "Earth intelligence and space infrastructure", "Public", "Public", 2017, "Westminster, CO"),
            c("BlackSky", "blacksky.com", "Real-time geospatial intelligence", "Public", "Public", 2014, "Herndon, VA"),
            c("Capella Space", "capellaspace.com", "SAR satellite earth observation", "$312M", "Late", 2016, "San Francisco, CA"),
            c("HawkEye 360", "he360.com", "RF analytics and geospatial intelligence", "$334M", "Late", 2015, "Herndon, VA"),
            c("Umbra", "umbra.space", "High-resolution SAR satellite imaging", "$85M", "Growth", 2015, "Santa Barbara, CA"),
        ]),
    ]),

    # ── 15. Robotics & Automation ──
    ind("robotics-automation", "Robotics & Automation", [
        sub("industrial-robotics", "Industrial Robotics", [
            c("Fanuc", "fanuc.com", "Factory automation and industrial robotics leader", "Public", "Public", 1972, "Oshino, Japan"),
            c("ABB Robotics", "abb.com", "Industrial robotics and automation solutions", "Public", "Public", 1988, "Zurich, Switzerland"),
            c("Covariant", "covariant.ai", "AI-powered robotic picking for warehouses", "$222M", "Growth", 2017, "Emeryville, CA"),
            c("Machina Labs", "machinalabs.ai", "AI-driven robotic sheet metal forming", "$58M", "Growth", 2019, "Los Angeles, CA"),
            c("Formic", "formic.co", "Robots-as-a-service for manufacturers", "$52M", "Growth", 2020, "Chicago, IL"),
        ]),
        sub("service-robotics", "Service Robotics", [
            c("Boston Dynamics", "bostondynamics.com", "Advanced mobile robots like Spot and Atlas", "Subsidiary", "Late", 1992, "Waltham, MA"),
            c("Bear Robotics", "bearrobotics.ai", "Autonomous restaurant service robots", "$81M", "Growth", 2017, "Redwood City, CA"),
            c("Serve Robotics", "serverobotics.com", "Autonomous sidewalk delivery robots", "Public", "Public", 2021, "Los Angeles, CA"),
            c("Savioke", "savioke.com", "Autonomous delivery robots for hospitality", "$38M", "Growth", 2013, "San Jose, CA"),
            c("Diligent Robotics", "diligentrobots.com", "Autonomous mobile robots for hospitals", "$47M", "Growth", 2017, "Austin, TX"),
        ]),
        sub("rpa", "RPA & Process Automation", [
            c("UiPath", "uipath.com", "Enterprise robotic process automation", "Public", "Public", 2005, "New York, NY"),
            c("Automation Anywhere", "automationanywhere.com", "Intelligent automation for enterprises", "$839M", "Late", 2003, "San Jose, CA"),
            c("Celonis", "celonis.com", "Process mining and execution management", "$1.4B", "Late", 2011, "Munich, Germany"),
            c("Workato", "workato.com", "Enterprise automation and integration platform", "$421M", "Late", 2013, "Mountain View, CA"),
            c("Tines", "tines.com", "No-code security workflow automation", "$126M", "Growth", 2018, "Dublin, Ireland"),
        ]),
        sub("warehouse-robotics", "Warehouse & Logistics Robotics", [
            c("Locus Robotics", "locusrobotics.com", "Autonomous mobile robots for warehouses", "$380M", "Late", 2014, "Wilmington, MA"),
            c("GreyOrange", "greyorange.com", "AI-driven fulfillment automation robotics", "$157M", "Growth", 2011, "Atlanta, GA"),
            c("Symbotic", "symbotic.com", "AI-powered warehouse automation systems", "Public", "Public", 2007, "Wilmington, MA"),
            c("Exotec", "exotec.com", "Robotic warehouse automation systems", "$335M", "Late", 2015, "Croix, France"),
            c("Nimble", "nimble.ai", "AI-driven robotic picking for e-commerce", "$65M", "Growth", 2017, "San Francisco, CA"),
        ]),
        sub("autonomous-systems", "Autonomous Systems", [
            c("Figure AI", "figure.ai", "General-purpose humanoid robots", "$754M", "Late", 2022, "Sunnyvale, CA"),
            c("Apptronik", "apptronik.com", "Humanoid robots for logistics and manufacturing", "$24M", "Early", 2016, "Austin, TX"),
            c("Agility Robotics", "agilityrobotics.com", "Bipedal warehouse robot Digit", "$179M", "Growth", 2015, "Corvallis, OR"),
            c("1X Technologies", "1x.tech", "Humanoid robots for everyday tasks", "$125M", "Growth", 2014, "Moss, Norway"),
            c("Sanctuary AI", "sanctuary.ai", "General-purpose humanoid robot Phoenix", "$159M", "Growth", 2018, "Vancouver, Canada"),
        ]),
    ]),

    # ── 16. Blockchain & Web3 ──
    ind("blockchain-web3", "Blockchain & Web3", [
        sub("defi", "Decentralized Finance (DeFi)", [
            c("Uniswap Labs", "uniswap.org", "Leading decentralized exchange protocol", "$176M", "Growth", 2018, "New York, NY"),
            c("Aave", "aave.com", "Decentralized lending and borrowing protocol", "$49M", "Growth", 2017, "London, UK"),
            c("MakerDAO", "makerdao.com", "Decentralized stablecoin DAI protocol", "$57M", "Growth", 2014, "Remote"),
            c("dYdX", "dydx.exchange", "Decentralized perpetuals exchange", "$87M", "Growth", 2017, "New York, NY"),
            c("Lido Finance", "lido.fi", "Liquid staking protocol for Ethereum", "$73M", "Growth", 2020, "Remote"),
        ]),
        sub("crypto-infra", "Crypto Infrastructure", [
            c("Alchemy", "alchemy.com", "Web3 development platform and APIs", "$345M", "Late", 2017, "San Francisco, CA"),
            c("Infura", "infura.io", "Blockchain API infrastructure by ConsenSys", "Subsidiary", "Late", 2016, "Remote"),
            c("QuickNode", "quicknode.com", "Web3 infrastructure and node services", "$120M", "Growth", 2017, "Miami, FL"),
            c("Blockdaemon", "blockdaemon.com", "Blockchain node infrastructure platform", "$155M", "Growth", 2017, "New York, NY"),
            c("Figment", "figment.io", "Blockchain infrastructure and staking services", "$100M", "Growth", 2018, "Toronto, Canada"),
        ]),
        sub("l1-l2", "Layer 1 & Layer 2 Protocols", [
            c("Ethereum Foundation", "ethereum.org", "Decentralized smart contract platform", "Non-profit", "Late", 2014, "Zug, Switzerland"),
            c("Solana Labs", "solana.com", "High-performance blockchain platform", "$336M", "Late", 2018, "San Francisco, CA"),
            c("Polygon", "polygon.technology", "Ethereum scaling and infrastructure", "$450M", "Late", 2017, "Remote"),
            c("Avalanche (Ava Labs)", "avax.network", "Fast, eco-friendly smart contract platform", "$290M", "Late", 2018, "Brooklyn, NY"),
            c("Arbitrum (Offchain Labs)", "arbitrum.io", "Ethereum Layer 2 rollup scaling solution", "$143M", "Growth", 2018, "Princeton, NJ"),
            c("StarkWare", "starkware.co", "Zero-knowledge proof scaling for Ethereum", "$263M", "Late", 2018, "Netanya, Israel"),
        ]),
        sub("nft-digital-assets", "NFT & Digital Assets", [
            c("OpenSea", "opensea.io", "Largest NFT marketplace", "$427M", "Late", 2017, "New York, NY"),
            c("Yuga Labs", "yuga.com", "Creator of Bored Ape Yacht Club", "$450M", "Late", 2021, "Miami, FL"),
            c("Dapper Labs", "dapperlabs.com", "Creator of NBA Top Shot and Flow blockchain", "$610M", "Late", 2018, "Vancouver, Canada"),
            c("Immutable", "immutable.com", "Web3 gaming platform and NFT infrastructure", "$280M", "Late", 2018, "Sydney, Australia"),
            c("Zora", "zora.co", "Decentralized NFT marketplace protocol", "$60M", "Growth", 2020, "Remote"),
        ]),
        sub("web3-gaming", "Web3 Gaming", [
            c("Sky Mavis", "skymavis.com", "Creator of Axie Infinity blockchain game", "$311M", "Late", 2018, "Ho Chi Minh City, Vietnam"),
            c("Animoca Brands", "animocabrands.com", "Web3 gaming and metaverse investments", "$589M", "Late", 2014, "Hong Kong"),
            c("Mythical Games", "mythicalgames.com", "Web3 game studio behind Blankos", "$260M", "Late", 2018, "Sherman Oaks, CA"),
            c("Horizon Blockchain Games", "horizon.io", "Web3 gaming infrastructure", "$120M", "Growth", 2017, "Toronto, Canada"),
            c("Proof of Play", "proofofplay.com", "On-chain game developer", "$43M", "Growth", 2022, "San Francisco, CA"),
        ]),
    ]),

    # ── 17. Legal & Compliance Tech ──
    ind("legal-compliance", "Legal & Compliance Tech", [
        sub("contract-mgmt", "Contract Management", [
            c("Icertis", "icertis.com", "Enterprise contract lifecycle management", "$296M", "Late", 2009, "Bellevue, WA"),
            c("DocuSign", "docusign.com", "E-signature and contract management", "Public", "Public", 2003, "San Francisco, CA"),
            c("Ironclad", "ironcladapp.com", "Digital contract management platform", "$233M", "Growth", 2014, "San Francisco, CA"),
            c("Juro", "juro.com", "AI-powered contract automation", "$33M", "Growth", 2016, "London, UK"),
            c("LinkSquares", "linksquares.com", "AI-powered contract analytics platform", "$100M", "Growth", 2015, "Boston, MA"),
        ]),
        sub("legal-research", "Legal Research & AI", [
            c("Casetext", "casetext.com", "AI legal research assistant CoCounsel", "$68M", "Growth", 2013, "San Francisco, CA"),
            c("Harvey", "harvey.ai", "AI assistant for legal professionals", "$106M", "Growth", 2022, "San Francisco, CA"),
            c("vLex", "vlex.com", "AI-powered legal research platform", "$24M", "Growth", 2001, "Barcelona, Spain"),
            c("EvenUp", "evenuplaw.com", "AI for personal injury demand letters", "$135M", "Growth", 2019, "San Francisco, CA"),
            c("Luminance", "luminance.com", "AI platform for legal document review", "$40M", "Growth", 2015, "London, UK"),
        ]),
        sub("regtech", "RegTech & Compliance", [
            c("ComplyAdvantage", "complyadvantage.com", "AI-driven AML and fraud detection", "$115M", "Growth", 2014, "New York, NY"),
            c("Chainalysis", "chainalysis.com", "Blockchain compliance and investigation", "$536M", "Late", 2014, "New York, NY"),
            c("Hummingbird", "hummingbird.co", "Anti-money laundering investigation platform", "$30M", "Growth", 2017, "New York, NY"),
            c("Ascent", "ascentregtech.com", "Regulatory knowledge automation", "$27M", "Growth", 2015, "Chicago, IL"),
            c("Sumsub", "sumsub.com", "Identity verification and compliance platform", "$61M", "Growth", 2015, "London, UK"),
        ]),
        sub("ediscovery", "E-Discovery & Litigation", [
            c("Relativity", "relativity.com", "E-discovery and legal review platform", "$555M", "Late", 2001, "Chicago, IL"),
            c("Everlaw", "everlaw.com", "Cloud-native e-discovery platform", "$231M", "Growth", 2010, "Oakland, CA"),
            c("Disco", "csdisco.com", "Cloud e-discovery and legal AI", "Public", "Public", 2013, "Austin, TX"),
            c("Reveal Data", "revealdata.com", "AI-powered e-discovery platform", "$57M", "Growth", 2007, "Houston, TX"),
            c("Logikcull", "logikcull.com", "Instant discovery for legal teams", "$30M", "Growth", 2004, "San Francisco, CA"),
        ]),
        sub("practice-mgmt", "Legal Practice Management", [
            c("Clio", "clio.com", "Cloud-based legal practice management", "$640M", "Late", 2008, "Vancouver, Canada"),
            c("MyCase", "mycase.com", "Law practice management software", "$65M", "Growth", 2010, "San Diego, CA"),
            c("Smokeball", "smokeball.com", "Legal practice management for small firms", "$30M", "Growth", 2012, "Chicago, IL"),
            c("PracticePanther", "practicepanther.com", "Law firm management software", "$20M", "Growth", 2012, "Miami, FL"),
            c("Litify", "litify.com", "Legal operating platform on Salesforce", "$30M", "Growth", 2016, "New York, NY"),
        ]),
    ]),

    # ── 18. HR & Future of Work ──
    ind("hr-future-work", "HR & Future of Work", [
        sub("recruiting", "Recruiting & Talent", [
            c("LinkedIn", "linkedin.com", "Professional network and recruiting platform", "Subsidiary", "Public", 2002, "Sunnyvale, CA"),
            c("Greenhouse", "greenhouse.io", "Hiring and applicant tracking platform", "$110M", "Late", 2012, "New York, NY"),
            c("Lever", "lever.co", "Talent acquisition and ATS platform", "$122M", "Growth", 2012, "San Francisco, CA"),
            c("Eightfold AI", "eightfold.ai", "AI talent intelligence platform", "$396M", "Late", 2016, "Santa Clara, CA"),
            c("HireVue", "hirevue.com", "Video interviewing and AI talent assessment", "$93M", "Growth", 2004, "South Jordan, UT"),
            c("Handshake", "joinhandshake.com", "Career network for college students", "$434M", "Late", 2014, "San Francisco, CA"),
        ]),
        sub("payroll-benefits", "Payroll & Benefits", [
            c("Gusto", "gusto.com", "Payroll, benefits, and HR for SMBs", "$746M", "Late", 2011, "San Francisco, CA"),
            c("Rippling", "rippling.com", "Unified HR, IT, and finance platform", "$1.2B", "Late", 2016, "San Francisco, CA"),
            c("Deel", "deel.com", "Global payroll and compliance for remote teams", "$679M", "Late", 2019, "San Francisco, CA"),
            c("Papaya Global", "papayaglobal.com", "Global payroll and workforce management", "$400M", "Late", 2016, "New York, NY"),
            c("Remote.com", "remote.com", "Global employment and payroll platform", "$496M", "Late", 2019, "San Francisco, CA"),
            c("Justworks", "justworks.com", "PEO and payroll platform for small businesses", "$164M", "Late", 2012, "New York, NY"),
        ]),
        sub("employee-exp", "Employee Experience", [
            c("Culture Amp", "cultureamp.com", "Employee experience and engagement platform", "$267M", "Late", 2011, "Melbourne, Australia"),
            c("Lattice", "lattice.com", "People management and performance platform", "$329M", "Late", 2015, "San Francisco, CA"),
            c("15Five", "15five.com", "Performance management and engagement", "$120M", "Growth", 2011, "San Francisco, CA"),
            c("Leapsome", "leapsome.com", "People enablement and performance platform", "$60M", "Growth", 2016, "Berlin, Germany"),
            c("Workvivo", "workvivo.com", "Employee communication and engagement platform", "$35M", "Growth", 2017, "Cork, Ireland"),
        ]),
        sub("workforce-mgmt", "Workforce Management", [
            c("Deputy", "deputy.com", "Shift scheduling and workforce management", "$115M", "Growth", 2008, "Sydney, Australia"),
            c("When I Work", "wheniwork.com", "Employee scheduling and time tracking", "$200M", "Growth", 2010, "Minneapolis, MN"),
            c("Personio", "personio.com", "All-in-one HR software for SMBs", "$722M", "Late", 2015, "Munich, Germany"),
            c("Quinyx", "quinyx.com", "AI-powered workforce management", "$100M", "Growth", 2005, "Stockholm, Sweden"),
            c("Legion Technologies", "legion.co", "AI-powered workforce management platform", "$151M", "Growth", 2016, "Palo Alto, CA"),
        ]),
        sub("freelance-gig", "Freelance & Gig Economy", [
            c("Upwork", "upwork.com", "Freelance talent marketplace", "Public", "Public", 2015, "San Francisco, CA"),
            c("Fiverr", "fiverr.com", "Freelance services marketplace", "Public", "Public", 2010, "Tel Aviv, Israel"),
            c("Toptal", "toptal.com", "Freelance talent network for top developers", "$44M", "Late", 2010, "Remote"),
            c("Contra", "contra.com", "Independent professional portfolio and jobs", "$44M", "Growth", 2020, "San Francisco, CA"),
            c("Braintrust", "usebraintrust.com", "Decentralized talent network", "$100M", "Growth", 2018, "San Francisco, CA"),
        ]),
    ]),

    # ── 19. Telecommunications & Connectivity ──
    ind("telecom-connectivity", "Telecommunications & Connectivity", [
        sub("5g-infra", "5G Infrastructure", [
            c("Qualcomm", "qualcomm.com", "5G chipsets and wireless technology leader", "Public", "Public", 1985, "San Diego, CA"),
            c("Ericsson", "ericsson.com", "Telecom infrastructure and 5G networks", "Public", "Public", 1876, "Stockholm, Sweden"),
            c("Nokia", "nokia.com", "Network infrastructure and 5G technology", "Public", "Public", 1865, "Espoo, Finland"),
            c("Mavenir", "mavenir.com", "Cloud-native 5G network software", "$155M", "Growth", 2005, "Richardson, TX"),
            c("Celona", "celona.io", "Private 5G network platform for enterprises", "$100M", "Growth", 2019, "Cupertino, CA"),
        ]),
        sub("ucaas-cpaas", "UCaaS & CPaaS", [
            c("Twilio", "twilio.com", "Cloud communications platform and APIs", "Public", "Public", 2008, "San Francisco, CA"),
            c("Vonage", "vonage.com", "Cloud communications and CPaaS platform", "Subsidiary", "Late", 2001, "Holmdel, NJ"),
            c("Bandwidth", "bandwidth.com", "Enterprise cloud communications APIs", "Public", "Public", 1999, "Raleigh, NC"),
            c("MessageBird", "messagebird.com", "Omnichannel communications platform", "$1.1B", "Late", 2011, "Amsterdam, Netherlands"),
            c("Sinch", "sinch.com", "Cloud communications for customer engagement", "Public", "Public", 2008, "Stockholm, Sweden"),
        ]),
        sub("satellite-comms", "Satellite Communications", [
            c("Starlink (SpaceX)", "starlink.com", "Global satellite internet constellation", "Subsidiary", "Late", 2015, "Hawthorne, CA"),
            c("OneWeb", "oneweb.net", "Low Earth orbit satellite broadband", "$3.4B", "Late", 2012, "London, UK"),
            c("Viasat", "viasat.com", "Satellite communications and services", "Public", "Public", 1986, "Carlsbad, CA"),
            c("AST SpaceMobile", "ast-science.com", "Space-based cellular broadband network", "Public", "Public", 2017, "Midland, TX"),
            c("Lynk Global", "lynk.world", "Satellite-to-phone connectivity", "$120M", "Growth", 2017, "Falls Church, VA"),
        ]),
        sub("iot-connectivity", "IoT Connectivity", [
            c("Samsara", "samsara.com", "IoT platform for operations and fleet", "Public", "Public", 2015, "San Francisco, CA"),
            c("Particle", "particle.io", "IoT device platform and connectivity", "$96M", "Growth", 2013, "San Francisco, CA"),
            c("Hologram", "hologram.io", "Cellular IoT connectivity platform", "$81M", "Growth", 2013, "Chicago, IL"),
            c("Blues", "blues.com", "Wireless IoT connectivity via Notecard", "$46M", "Growth", 2019, "Boston, MA"),
            c("Soracom", "soracom.io", "Global IoT connectivity platform", "$90M", "Growth", 2015, "Tokyo, Japan"),
        ]),
        sub("network-mgmt", "Network Management & Security", [
            c("Fortinet", "fortinet.com", "Network security and firewall solutions", "Public", "Public", 2000, "Sunnyvale, CA"),
            c("Arista Networks", "arista.com", "Cloud networking and switches", "Public", "Public", 2004, "Santa Clara, CA"),
            c("Cato Networks", "catonetworks.com", "Cloud-native SASE platform", "$773M", "Late", 2015, "Tel Aviv, Israel"),
            c("Versa Networks", "versa-networks.com", "Secure SD-WAN and SASE platform", "$196M", "Growth", 2012, "Santa Clara, CA"),
            c("Alkira", "alkira.com", "Cloud network-as-a-service platform", "$76M", "Growth", 2018, "San Jose, CA"),
        ]),
    ]),

    # ── 20. Consumer & Social ──
    ind("consumer-social", "Consumer & Social", [
        sub("social-community", "Social Media & Community", [
            c("Reddit", "reddit.com", "Social news and community platform", "Public", "Public", 2005, "San Francisco, CA"),
            c("Discord", "discord.com", "Community platform for voice and text chat", "$982M", "Late", 2012, "San Francisco, CA"),
            c("BeReal", "bereal.com", "Authentic social media photo sharing app", "$115M", "Growth", 2020, "Paris, France"),
            c("Lemon8", "lemon8-app.com", "Lifestyle content and community platform", "Subsidiary", "Late", 2020, "Singapore"),
            c("Geneva", "geneva.com", "Group chat and community platform", "$24M", "Growth", 2020, "New York, NY"),
        ]),
        sub("personal-finance", "Personal Finance", [
            c("Mint (Intuit)", "mint.com", "Personal finance and budgeting app", "Subsidiary", "Late", 2006, "Mountain View, CA"),
            c("Credit Karma", "creditkarma.com", "Free credit scores and financial tools", "Subsidiary", "Late", 2007, "Oakland, CA"),
            c("YNAB", "ynab.com", "Zero-based personal budgeting software", "$100M", "Growth", 2004, "Lehi, UT"),
            c("Monarch Money", "monarchmoney.com", "Modern personal finance and budgeting", "$34M", "Growth", 2019, "San Francisco, CA"),
            c("Copilot Money", "copilot.money", "Smart personal finance tracker for iOS", "$8M", "Early", 2020, "New York, NY"),
        ]),
        sub("health-wellness", "Health & Wellness", [
            c("Peloton", "onepeloton.com", "Connected fitness equipment and classes", "Public", "Public", 2012, "New York, NY"),
            c("Whoop", "whoop.com", "Wearable fitness and health tracker", "$405M", "Late", 2012, "Boston, MA"),
            c("Oura", "ouraring.com", "Smart ring for health and sleep tracking", "$148M", "Growth", 2013, "Oulu, Finland"),
            c("Noom", "noom.com", "Psychology-based weight loss program", "$594M", "Late", 2008, "New York, NY"),
            c("Levels", "levels.link", "Continuous glucose monitoring for metabolic health", "$74M", "Growth", 2019, "New York, NY"),
            c("Eight Sleep", "eightsleep.com", "Smart mattress and sleep technology", "$175M", "Growth", 2014, "New York, NY"),
        ]),
        sub("travel-tech", "Travel Tech", [
            c("Airbnb", "airbnb.com", "Global home-sharing and travel platform", "Public", "Public", 2008, "San Francisco, CA"),
            c("Booking.com", "booking.com", "Online travel agency and hotel booking", "Public", "Public", 1996, "Amsterdam, Netherlands"),
            c("Hopper", "hopper.com", "AI-powered travel booking and price prediction", "$700M", "Late", 2007, "Montreal, Canada"),
            c("Flyr", "flyrlabs.com", "AI revenue management for airlines", "$175M", "Growth", 2013, "San Francisco, CA"),
            c("Wheel the World", "wheeltheworld.com", "Accessible travel booking platform", "$8M", "Early", 2018, "San Francisco, CA"),
            c("Selina", "selina.com", "Hospitality for digital nomads and travelers", "$340M", "Late", 2014, "Tel Aviv, Israel"),
        ]),
        sub("dating", "Dating & Relationships", [
            c("Match Group", "matchgroup.com", "Parent of Tinder, Hinge, Match.com", "Public", "Public", 1995, "Dallas, TX"),
            c("Bumble", "bumble.com", "Women-first dating and social networking", "Public", "Public", 2014, "Austin, TX"),
            c("Hinge", "hinge.co", "Dating app designed to be deleted", "Subsidiary", "Late", 2012, "New York, NY"),
            c("Thursday", "getthursday.com", "Dating app that works one day a week", "$5M", "Early", 2021, "London, UK"),
            c("Feeld", "feeld.co", "Dating app for open-minded people", "$10M", "Growth", 2014, "London, UK"),
        ]),
    ]),
]

# Write JSON
data = {"industries": industries}
with open("/Users/spencerweinhoff/Desktop/sec-to-excel/industry_data.json", "w") as f:
    json.dump(data, f, indent=2)

# Count
total = sum(len(co) for ind in industries for sub in ind["sub_industries"] for co in [sub["companies"]])
companies = sum(len(sub["companies"]) for ind in industries for sub in ind["sub_industries"])
print(f"Written {len(industries)} industries, {sum(len(i['sub_industries']) for i in industries)} sub-industries, {companies} companies")
