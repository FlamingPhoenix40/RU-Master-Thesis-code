function estimateBlockingTime() {
    console.log("estimateBlockingTime function executing...");

    const performanceEntries = performance.getEntriesByType("navigation");
    
    if (performanceEntries.length === 0) {
        console.log("No navigation entries found");
        return;
    }

    const navigationEntry = performanceEntries[0];

    const startTime = navigationEntry.startTime;
    const loadEventEnd = navigationEntry.loadEventEnd;
    const estimatedTBT = (loadEventEnd - startTime) * 0.6;

    console.log("Estimated Total Blocking Time: ", estimatedTBT);

    return estimatedTBT;
}

const estimatedTBT = estimateBlockingTime();
return estimatedTBT;