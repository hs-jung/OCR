const ocrSpaceApi = require('ocr-space-api');
 
var options =  { 
    apikey: 'K84102663288957',
    language: 'eng', // Português
    imageFormat: 'image/jpeg', // Image Type (Only png ou gif is acceptable at the moment i wrote this)
    isOverlayRequired: true,
    OCREngine: 2
  };
 
// Image file to upload
const imageFilePath = "../assets/test1-1.jpeg";
 
// Run and wait the result
ocrSpaceApi.parseImageFromLocalFile(imageFilePath, options)
  .then(function (parsedResult) {
    console.log('parsedText: \n', parsedResult.parsedText);
    console.log('ocrParsedResult: \n', parsedResult.ocrParsedResult);
  }).catch(function (err) {
    console.log('ERROR:', err);
  });
