# Cloud_TP3

### TASK 1
Criando files `pyfile.yaml`, `outputkey.yaml`, `requirements.yaml`
```
kubectl create configmap pyfile --from-file pyfile=function.py --output yaml > pyfile.yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=leonardooliveira-proj3-output --output yaml > outputkey.yaml
kubectl apply -f deployment.yaml
```
Deletando pod
```
kubectl delete deploy serverless-redis
```
Deletando arquivos no namespace
```
kubectl delete configmap pyfile
kubectl delete configmap outputkey
```