<div align="center">
  <h1>Snatch</h1>
  <h3>AI OSINT - Capture, download, and enjoy.</h3>
  <img src="https://img.shields.io/badge/Python-purple?style=for-the-badge&logo=python&logoColor=white"/> 
  <a href="https://github.com/FJRG2007"> <img alt="GitHub" src="https://img.shields.io/badge/GitHub-purple?style=for-the-badge&logo=github&logoColor=white"/></a>
  <a href="https://ko-fi.com/fjrg2007"> <img alt="Kofi" src="https://img.shields.io/badge/Ko--fi-purple?style=for-the-badge&logo=ko-fi&logoColor=white"></a>
  <br />
  <br />
  <a href="https://github.com/FJRG2007/snatch/blob/main/docs/getting-started/quickstart.md">Quickstart</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="https://tpeoficial.com/dsc">Discord</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="https://github.com/FJRG2007/snatch/blob/main/docs/community/features.md">All Features</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="https://github.com/FJRG2007/snatch/blob/main/docs/REQUIREMENTS.md">Requirements</a>
  <span>&nbsp;&nbsp;•&nbsp;&nbsp;</span>
  <a href="https://github.com/FJRG2007/snatch/blob/main/docs/community/FAQ.md">FAQ</a>
  <br />
  <hr />
</div>

**Snatch** is a versatile tool crafted for cybersecurity and hacking enthusiasts. Developed in Python and currently in active development, **Snatch** aims to serve as a powerful multipurpose tool for OSINT (Open Source Intelligence) tasks, leveraging Artificial Intelligence to enhance task efficiency and speed.

Imagine simply inputting a prompt that details all relevant information about your target. **Snatch** then autonomously generates potential password lists, identifies possible emails and social networks, and more.

Alternatively, you can directly execute commands via your terminal to utilize **Snatch**.

It's important to emphasize that **Snatch** is a work in progress, and all operations are conducted locally. Users should exercise caution as they assume full responsibility for their actions.

**Disclaimer**: This tool are for technical discussion and sharing only. Illegal use is strictly prohibited.

<img src="./docs/images/basic-diagram.jpeg" loading="lazy" />

### Use (for development)

First clone the repository:
```bash
$ git clone https://github.com/FJRG2007/snatch.git
$ cd snatch
```

Now install the requirements:
```bash
$ pip install -r requirements.txt
```

Then, replace the `.env.example` file to `.env` and fill in the tokens you need.
```bash
# For production (not available yet).
$ snatch help
# For development (replace snatch with python cli.py).
$ python cli.py help
```

### Main Features (Modules)

| Name                              | Status              | Active |
|-----------------------------------|---------------------|--------|
| AI Prompt                         | In development      |   ⚠️   |
| OSINT Automation	                | Coming Soon	        |   ❌   |
| Vulnerability Scanning Algorithm  | Coming Soon         |   ❌   |
| Data Search & Completion Tool     | In BETA Phase       |   ⚠️   |
| Ports Scanner                     | Active              |   ✅   |
| Website/video/data Downloader     | Active              |   ✅   |
| Directory & Subdomain Listing     | Active              |   ✅   |
| Password List Generation          | Active              |   ✅   |
| WhatsApp Basic OSINT              | Active              |   ✅   |
| Wifi Scanner                      | Relatively Soon     |   ❌   |
| Image Analysis	                  | In development	    |   ⚠️   |
| Dark Web Monitoring	              | Coming Soon	        |   ❌   |
| Metadata Extractor	              | In development	    |   ⚠️   |
| Personal Data Scraper             | In development      |   ⚠️   |

[All Features](./docs/community/features.md)

> [!IMPORTANT]\
> Due to the sensitive nature of OSINT tools, full versions of some tools will not be provided. For example, the WhatsApp LOGS tool is only available in a basic version.

### Supported AI Models

| Provider                       | Models (Assorted)                             | Execution   | Rating  |
|--------------------------------|-----------------------------------------------|-------------|---------|
| Anthropic                      | Claude                                        | API         | None    |
| TPEOficial                     | Dymo AGI, ELA                                 | API         | None    |
| Google                         | Gemini                                        | API         | None    |
| Groq                           | Llama3, Gemma, Whisper                        | API         | None    |
| Meta                           | Llama3                                        | API         | None    |
| Ollama                         | Llama3, Gemma                                 | Local       | None    |
| OpenAI                         | GPT-4o, GPT-4, GPT-3.5 Turbo, GPT-3.5         | API         | None    |
| Perplexity                     | Llama3, Mixtral                               | API         | None    |

Requirements available at [`REQUIREMENTS`](./docs/REQUIREMENTS.md).

#### Author
 - FJRG007
 - Email: [fjrg2007@tpeoficial.com](mailto:fjrg2007@tpeoficial.com)

#### Contributors
To contribute to the project visit the requirements at [`CONTRIBUTING`](./docs/dev/CONTRIBUTING.md).

![Alt](https://repobeats.axiom.co/api/embed/752f1062974e1799dfb603d420343078a9e4a378.svg "Snatch analytics image")

**Note**: If you are a contributor and do not appear here, wait a little while until the image is reloaded.

#### License
The founder of the project, [FJRG2007](https://github.com/FJRG2007/), reserves the right to modify the license at any time.
This project is licensed under the terms of the [GNU Affero General Public License](./LICENSE).