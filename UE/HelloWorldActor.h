#pragma once

#include "CoreMinimal.h"
#include "GameFramework/Actor.h"
#include "HelloWorldActor.generated.h"

UCLASS()
class YOURPROJECT_API AHelloWorldActor : public AActor
{
    GENERATED_BODY()

public:	
    AHelloWorldActor();

protected:
    virtual void BeginPlay() override;
};