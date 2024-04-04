function getContentfulPaints() {
    const paintTimings = performance.getEntriesByType("paint");
    const fcpEntry = paintTimings.find(entry => entry.name === "first-contentful-paint");
  
    return {
      fcp: fcpEntry ? fcpEntry.startTime : null,
    };
  }
  
  // Call the function and return the FCP value
  return getContentfulPaints(); 
  