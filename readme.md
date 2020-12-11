# 50.007 Machine Learning Project
## PART 2 Simple sentiment analysis
In order to run simple sentiment analysis predictions, use the code below
```
python run.py -m simple_sentiment -p ./data/CN
```
Replace "CN" with "EN" and "SG" to do predictions with other dataset.
### **Evaluation Entity**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.0812    | 0.4929 | 0.1395 |
| EN | 0.5116    | 0.7240 | 0.5996 |
| SG | 0.1950   | 0.5548 | 0.2885 |

### **Evaluation Sentiment**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.0393    | 0.2386 | 0.0675 |
| EN | 0.4534    | 0.6416 | 0.5313 |
| SG | 0.1251   | 0.3560 | 0.1851 |
## PART 3 Viterbi Algorithm
In order to run viterbi sentiment analysis predictions, use the code below
```
python run.py -m viterbi -p ./data/CN
```
Replace "CN" with "EN" and "SG" to do predictions with other dataset.
### **Evaluation Entity**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.2461    | 0.2914 | 0.2668 |
| EN |  0.7446    | 0.8069 | 0.7745 |
| SG | 0.4837    | 0.5155 | 0.4991 |
### **Evaluation Sentiment**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.1460    | 0.1729 | 0.1583 |
| EN | 0.6775    | 0.7342 |  0.7047 |
| SG | 0.3945  | 0.4204 | 0.4070 |

## PART 4 Viterbi top kth Algorithm
In order to run viterbi 3rd best sequence sentiment analysis predictions, use the code below
```
python run.py -m viterbi_top_k -p ./data/CN
```
Replace "CN" with "EN" and "SG" to do predictions with other dataset.
### **Evaluation Entity**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.1368    |0.3086 | 0.1896 |
| EN |  0.7994    |0.7564 | 0.7773 |
| SG |0.4183   |0.4729| 0.4440 |
### **Evaluation Sentiment**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.0766   | 0.1729| 0.1062 |
| EN |  0.7638   | 0.7227 |  0.7426|
| SG | 0.2879  |0.3255 | 0.3056|

## Evluation script
Run evaluation script by going into eval folder
```
python evalResult.py <actual data path> <predicted data path>
```
