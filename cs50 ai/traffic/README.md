# Model Exploration and Optimization

## Initial Model
I first started with the model that was built in the lecture to figure out the numbers from different handwritten digits. I adjusted the network a bit to have the correct number of outputs and made the convolutional layer less complex. However, I was only achieving about 0.05 accuracy.

## Optimized Network with ChatGPT's Assistance
Next, I asked ChatGPT to help me create an optimized network for my requirements, and I'm now getting around 0.97 accuracy. What I noticed was that ChatGPT added two additional convolutional layers and two more pooling layers. This approach of convoluting and pooling multiple times is crucial for handling complex image classifications like this one. Additionally, it added two more hidden layers with 128 units for the first and 64 units for the second. GPT suggested using a dropout rate of 0.3 for both hidden networks, as a 0.5 dropout rate might lead to underfitting in this scenario. The output layer and the compiler settings were left the same.

## Activation Functions and Output Layer
It's worth noting that all the activation functions are ReLU, except for the output layer, which uses softmax. This choice makes sense because this is a classification problem, and softmax helps in assigning probabilities to different classes. If the output values before a certain threshold are x and after are abcd..., using softmax is a suitable choice for classification.

## Conclusion
While part of me thinks that I should experiment a bit more, another part of me, perhaps the more relaxed and pragmatic programmer part, believes that I've provided a solution that works, and a method that does not. I've also provided reasons for why it should or shouldn't work, and experimenting just for the sake of it without a clear goal in mind (like optimize this network) is not my strong suit. I hope this explanation is sufficient.
