# Codable PPTX

## Dependencies
- Python 3.7.6
- PyYAML
- Pillow
- python-pptx

## Install Dependencies

```sh
pip install -r requirements.txt
```

## Usage

```sh
sh presentation.sh <INPUT_YAML_FILE> <OUTPUT_PPTX_FILE>
```

## Sample

### Input
```yaml:slides.yaml
slides:
  - centerTitle: "Tokyo Yakult Swallows"
  - topTitle: "What are Swallows?"
    text: "The GREATEST Japanese baseball team"
  - topTitle: "Jingu Stadium"
    img: "jingu.jpeg"
  - sideTitle: "Testuto Yamada"
    sideImg: "yamada.jpeg"
  - sideTitle: "Norichika Aoki"
    sideImg: "aoki.jpeg"
  - sideTitle: "Munetaka Murakami"
    sideImg: "murakami.jpeg"
  - topTitle: "Why are Swallows so good?"
    text: |-
      The great stadium in a good location
      A lot of star players
```

### Output
![slide1](https://github.com/liwii/CodablePPTX/blob/images/images/test-1.png?raw=true)
![slide2](https://github.com/liwii/CodablePPTX/blob/images/images/test-2.png?raw=true)
![slide3](https://github.com/liwii/CodablePPTX/blob/images/images/test-3.png?raw=true)
![slide4](https://github.com/liwii/CodablePPTX/blob/images/images/test-4.png?raw=true)
![slide5](https://github.com/liwii/CodablePPTX/blob/images/images/test-5.png?raw=true)
![slide6](https://github.com/liwii/CodablePPTX/blob/images/images/test-6.png?raw=true)
![slide7](https://github.com/liwii/CodablePPTX/blob/images/images/test-7.png?raw=true)
