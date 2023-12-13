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
Para ver se esta correto, verifique os logs.
```
kubectl get pods
kubectl logs <name pod>
```
### TASK 2
Usamos `git actions` para atualizar a imagem do dockerhub.


Deletando pod e servico
```
kubectl delete svc dashboard-service
kubectl delete deploy dashboard
```

Criando pod e serviço.
```
kubectl -n leonardomaia apply -f deployment.yaml -f service.yaml
```