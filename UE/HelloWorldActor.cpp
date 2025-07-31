#include "HelloWorldActor.h"
#include "Engine/Engine.h"

AHelloWorldActor::AHelloWorldActor()
{
    PrimaryActorTick.bCanEverTick = false;
}

void AHelloWorldActor::BeginPlay()
{
    Super::BeginPlay();
    
    // Print to Log
    UE_LOG(LogTemp, Warning, TEXT("Hello World from Unreal Engine 5!"));
    
    // Print to Screen
    if (GEngine)
    {
        GEngine->AddOnScreenDebugMessage(
            -1,                   // Key (use -1 to not overwrite)
            5.f,                  // Display time (seconds)
            FColor::Green,        // Text color
            TEXT("Hello World!")  // Message
        );
    }
}