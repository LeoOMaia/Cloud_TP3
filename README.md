# Cloud_TP3

### TASK 1
Deletando pod e arquivos no namespace
```
kubectl delete deploy serverless-redis
kubectl delete configmap pyfile
kubectl delete configmap outputkey
```
Criando files `pyfile.yaml`, `outputkey.yaml`, `requirements.yaml`
```
kubectl create configmap pyfile --from-file pyfile=function.py --output yaml > pyfile.yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=leonardooliveira-proj3-output --output yaml > outputkey.yaml
kubectl -n leonardomaia apply -f deployment.yaml
```
### TASK 2
Usamos git actions para atualizar a imagem do dockerhub.

```
kubectl -n leonardomaia apply -f deployment.yaml -f service.yaml
```