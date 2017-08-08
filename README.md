<h1> About </h1>

This project is a compilation of basic text analysis tools to understand and analyze German texts. As an example the project focuses on programmatic texts for the German parliament elections 1949 - 2017. 

<h1> Install </h1>

<h2> Docker </h2>
Kindly install via cloning and generating the Docker container.

Clone the repository first. Will take several minutes based on your connection bandwidth!!!

```
git clone https://github.io/chris1869/policy_analysis
```

Create the docker container:

```
docker build -t policy-analysis .
```

Run initial test to verify installation:

```
docker run policy-analysis
```
<h2> Manual installation (not tested) </h2>

<h1> Acknowledgments </h1>

Many thanks to all contributors of the third party packages that are used in this project. You made these analyses as convenient as possible.

<h3> Wordcloud </h3>
https://github.com/amueller/word_cloud

<h3> Readability </h3>
https://pypi.python.org/pypi/readability

<h3> Ucto </h3>
https://proycon.github.io/LaMachine/

<h3> Treetagger </h3>
http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/

<h3> Tiger Annotation Schema - POS </h3>
Some more information on the position of speech (POS) tags can be found on (Tiger Annotation Schema):

https://www.linguistik.hu-berlin.de/de/institut/professuren/korpuslinguistik/mitarbeiter-innen/hagen/STTS_Tagset_Tiger

<h3> Election programs 1949 - 2017 </h3>

Many thanks to the German parties and their respective endowments for providing the PDFs of the election programs online. In the future, a verified text of the older PDF scans would be great.

<h1> Disclaimer </h1>

This project wants to promote adoption of open source text analyses tools for German texts. There is no intend to judge, evaluate or comment on election programs. My hope is that it promotes a wider interest in the historic changes that drove election programs, better understand historic context and promotes reading the current election programs.

From what I was reading, the PDFs provided by parties and endowments the PDFs can be used for non-commercial reasons as is. Kindly approach me if this is not the case.