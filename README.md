# UMN_Prelim_NSCI_Math_Review
Review of mathematical neuroscience topics for the UMN Neurosci prelim

## ROC Curves
![ROC](https://github.com/alailink/UMN_Prelim_NSCI_Math_Review/blob/master/photos/ROC.gif)

The ROC curve assumes a few things:
* You have two distributions. In health sciences, this might be sick vs. healthy. In Neuroscience, this could be a 400Hz frequency vs. a 450Hz frequency.
* You have a classifier that discriminates based on a 1-dimensional factor. This limitation is somewhat arbitrary as you can use a data-reduction method to get one dimension, such as a principal component (PCA). 

The curve itself is a two dimensional summary of how well your classifier can discriminate between those two different distributions, as a function of the *discrimination line*. Its output is the true positive rate vs the false positive rate.  
The ROC's usefulness is in this discrimination line and how you might want to alter it according to different circumstances:  
* For COVID-19 screening, you might be okay with a high FPR, because you absolutely don't want to miss any sick patients. In other words, you can increase the TPR at the cost of also increasing the FPR.
* For bio-identification, you might be okay with a low TPR, such as having to scan your phone fingerprint a few times. This is because you absolutely don't want anyone else able to get on your phone. In other words, you can decrease the FPR at the cost of decreasing the TPR.  

The ROC curve is the standard metric in part because in machine-learning classification tasks, you can skew the TPR/FPR to make your research look better (harder when showing ROC). In addition, it's much like looking at a scatterplot instead of a bargraph. Scientists don't like the data summarized too much.  
A common practice is to report the 0.8 TPR and corresponding FPR.

## Cross Correlation
![CC](https://github.com/alailink/UMN_Prelim_NSCI_Math_Review/blob/master/photos/Cross-correlation.gif)  
Why do we need this metric in Neuroscience?  
We cannot compare two spike trains directly, because we are looking at different neurons and possible different regions of the brain. But by *sliding* the spike trains across each other, we can determine if there is a relationship even if they are not firing at the same time.  

How is the metric computed?
* Take a reference spike train and a target spike train
* slide the target across the reference, comparing only where the reference has neuron activity spikes
* Take the sum at each point and graph it. Possibly normalize.
* Y axis : coincidences / spikes / normalized counts
* X axis : sampling point of *sliding* 

![Singer W, Gray CM. Visual feature integration and the temporal correlation
hypothesis. Ann. Rev. Neurosci. 18: 555-86, 1995.](https://github.com/alailink/UMN_Prelim_NSCI_Math_Review/blob/master/photos/neuron-cc.PNG)  
The graphs on the left shows two spike trains that are highly correlated, as evidenced by the rise in coincidence near the center (but a rise anywhere would indicate correlation.)  
The graphs on the right show spike trains that are not correlated, as evidenced by a relatively flat line throughout, showing only spurious, random correlations.


