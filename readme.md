# 50.007 Machine Learning Project
## Simple sentiment analysis
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
## Viterbi Algorithm
In order to run simple sentiment analysis predictions, use the code below
```
python run.py -m viterbi -p ./data/CN
```
Replace "CN" with "EN" and "SG" to do predictions with other dataset.
### Evaluation
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.1549    | 0.3200 | 0.2088 |
| EN |  0.7446    | 0.8069 | 0.7745 |
| SG | 0.4837    | 0.5155 | 0.4991 |
### **Evaluation Sentiment**
|    | Precision | Recall | F1     |
|----|-----------|--------|--------|
| CN | 0.0837    | 0.1729 | 0.1128 |
| EN | 0.6775    | 0.7342 |  0.7047 |
| SG | 0.3945  | 0.4204 | 0.4070 |