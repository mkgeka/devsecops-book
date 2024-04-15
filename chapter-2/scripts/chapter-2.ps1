###
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogPortfolio.yml --stack-name EKSPortfolio --parameters file://chapter-2/parameter/ServiceCatalog.json --capabilities CAPABILITY_NAMED_IAM --region ca-central-1
#aws cloudformation update-stack --template-body file://chapter-2/template/ServiceCatalogPortfolio.yml --stack-name EKSPortfolio --parameters file://chapter-2/parameter/ServiceCatalog.json --capabilities CAPABILITY_NAMED_IAM --region ca-central-1
#aws s3 cp chapter-2/product/ s3://mkgeka-devopssec/ --recursive --exclude "*" --include "*.yml" --include "*.zip" --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSNetwork --parameters file://chapter-2/parameter/NetworkProduct.json --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSIAM --parameters file://chapter-2/parameter/IAMProduct.json --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSCluster --parameters file://chapter-2/parameter/EKSProduct.json --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSNodegroup --parameters file://chapter-2/parameter/EKSNodeGroupProduct.json --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSLambda --parameters file://chapter-2/parameter/EKSLambdaProduct.json --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSVPCendpoint --parameters file://chapter-2/parameter/VPCEndpointProduct.json --region ca-central-1
aws cloudformation create-stack --template-body file://chapter-2/template/ServiceCatalogProduct.yml --stack-name EKSLog --parameters file://chapter-2/parameter/EKSLoggingProduct.json --region ca-central-1
$PRODUCTID = aws servicecatalog describe-product --name DEV-eks-provisioner-product-ca-central-1 --region ca-central-1 --query ProductViewSummary.ProductId --output text
$PROVISIONARTIFACTID = aws servicecatalog describe-product --name DEV-eks-provisioner-product-ca-central-1 --region ca-central-1 --query 'ProvisioningArtifacts[0].Id' --output text
#aws servicecatalog provision-product --provisioned-product-name "eks-provision" --provisioning-artifact-id $PROVISIONARTIFACTID --product-id $PRODUCTID --provisioning-parameters file://chapter-2/parameter/eks-provisioner.json --profile default --region ca-central-1
#aws cloudformation delete-stack --stack-name EKSPortfolio --region ca-central-1
#aws cloudformation delete-stack --stack-name EKSNetwork --region ca-central-1
#aws cloudformation delete-stack --stack-name EKSIAM --region ca-central-1
#aws cloudformation delete-stack --stack-name EKSCluster --region ca-central-1