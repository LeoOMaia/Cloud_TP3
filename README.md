# Cloud_TP3
Para cada task, os comandos devem ser executados dentro de suas respectivas pastas.
### TASK 1
Deletando pod e arquivos no namespace se existirem.
```
kubectl delete deploy serverless-redis
kubectl delete configmap pyfile
kubectl delete configmap outputkey
```
Criando files `pyfile.yaml`, `outputkey.yaml` e seus respectivos configmap, e criando pod.
```
kubectl create configmap pyfile --from-file pyfile=function.py --output yaml > pyfile.yaml
kubectl create configmap outputkey --from-literal REDIS_OUTPUT_KEY=leonardooliveira-proj3-output --output yaml > outputkey.yaml
kubectl -n leonardomaia apply -f deployment.yaml
```
Para ver se esta correto, verifique se chegou informacao.
```
redis-cli
GET leonardooliveira-proj3-output
```
### TASK 2
Usamos `git actions` para atualizar a imagem do dockerhub.

Subindo servico
```
kubectl -n leonardomaia apply -f service.yaml
```
Criando ou Renovando pod
```
kubectl delete deploy dashboard
kubectl -n leonardomaia apply -f deployment.yaml
```