package lambda;

import com.amazonaws.auth.EnvironmentVariableCredentialsProvider;
import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.rekognition.AmazonRekognition;
import com.amazonaws.services.rekognition.AmazonRekognitionClientBuilder;
import com.amazonaws.services.rekognition.model.*;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.model.CopyObjectRequest;
import com.amazonaws.services.s3.model.DeleteObjectRequest;
import com.amazonaws.services.s3.model.ListObjectsV2Result;
import com.amazonaws.services.s3.model.S3ObjectSummary;
import model.LambdaParameters;

import java.text.SimpleDateFormat;
import java.util.*;

public class S3ImageCreateLambda implements RequestHandler<S3Event, LambdaParameters> {

  private LambdaParameters parameters;
  private AmazonRekognition amazonRekognitionClient;
  private String region = "us-east-1";
  private String familyPrefix = "family";
  private String humanPrefix = "humanFound";
  private float similarityThreshold = 90;
  private AmazonS3 s3Client;
  private String oldKey;
  private String bucketName;
  private int maxLabels = 10;
  private float minLabelConfidence = 90F;
  private Context context;
  private String newKey;


  public LambdaParameters handleRequest(S3Event s3Event, Context context) {
    this.context = context;
    context.getLogger()
        .log("Input Function [" + context.getFunctionName() + "], S3Event [" + s3Event.toJson().toString() + "]");
    s3Client = AmazonS3ClientBuilder
        .standard()
        .withCredentials(new EnvironmentVariableCredentialsProvider())
        .withRegion(region)
        .build();
    amazonRekognitionClient = AmazonRekognitionClientBuilder.defaultClient();
    parameters = setLambdaparameters(s3Event);
    context.getLogger().log("S3 upload parameter values " + parameters.toString());
    System.out.println("S3 Upload parameters : " + parameters.toString());

    Set<String> actualLabels = detectLabels(parameters);
    if (actualLabels != null) {
      if (isHumanDetected(actualLabels)) {
        context.getLogger().log("Human detected in image.");
        parameters.setHumanFound(true);
        parameters = isFamilyMemberFound(parameters) ?
            copyImageToFamily(parameters) : copyImageToHuman(parameters);
        deleteFromOrigin();
        parameters.setS3Key(newKey);
        context.getLogger().log(parameters.toString());
        System.out.println(parameters.toString());
      } else {
        context.getLogger().log("Human not detected in image");
        context.getLogger().log("Human not detected in image.");
        System.out.println(parameters.toString());
      }
    } else {
      context.getLogger().log("Lambda Parameters : " + parameters.toString());
      System.out.println(parameters.toString());
    }
    return parameters;
  }

  /**
   * Deletes image from origin after copying to "Human" or "familyVisit" folder
   */
  private void deleteFromOrigin() {
    DeleteObjectRequest deleteObjectRequest = new DeleteObjectRequest(bucketName, oldKey);
    s3Client.deleteObject(deleteObjectRequest);
  }

  /**
   * Copy image to human folder
   * @param parameters lambda parameters
   * @return updated lambda parameters
   */
  private LambdaParameters copyImageToHuman(LambdaParameters parameters) {
//    String newKey = getTodayDate() + "/" + parameters.getS3Key();
    newKey = humanPrefix + "/" + parameters.getS3Key();
    context.getLogger().log("Human - new key : " + newKey);
    System.out.println("Human - new key : " + newKey);
    CopyObjectRequest copyObjectRequest = new CopyObjectRequest(
        bucketName, oldKey, bucketName, newKey);
    s3Client.copyObject(copyObjectRequest);
    parameters.setFamilyMemberFound(false);
    context.getLogger().log("Object copied to \"" + humanPrefix + "\" folder.");
    return parameters;
  }

  /**
   * Determine whether detected label contains one of the expected lables
   * @param actualLabels labels detected after AWSRekogition
   * @return true if one of the human label found else false.
   */
  private boolean isHumanDetected(Set<String> actualLabels) {
    List<String> expectedLables = Arrays.asList("Human", "Person", "Child",
        "People", "Kid", "Girl", "Female");
    return actualLabels.stream().anyMatch(new HashSet<>(expectedLables)::contains);
  }

  /**
   * Detects label in  given image using AWS Rekognition
   * @param parameters lambda parameters
   * @return list of labels found after rekognition
   */
  private Set<String> detectLabels(LambdaParameters parameters) {
    try {
      DetectLabelsRequest request = new DetectLabelsRequest()
          .withImage(new Image().withS3Object(
              new S3Object().withName(parameters.getS3Key()).withBucket(parameters.getBucketName())))
          .withMaxLabels(maxLabels)
          .withMinConfidence(minLabelConfidence);
      DetectLabelsResult result = amazonRekognitionClient.detectLabels(request);
      List<Label> labels = result.getLabels();
      Set<String> actualLabels = new HashSet<>();
      for (Label label : labels) {
        actualLabels.add(label.getName());
      }
      return actualLabels;
    } catch (InvalidS3ObjectException e) {
      e.printStackTrace();
      System.out.println(e.getMessage());
      context.getLogger().log("Invalid S3 key.");
      System.out.println("Invalid S3 key.");
      return null;
    }
  }

//  public String getTodayDate() {
//    SimpleDateFormat formatter = new SimpleDateFormat("dd-MM-yyyy");
//    Date date = new Date();
//    return formatter.format(date);
//  }

  /**
   * Initialize lambda parameters with s3 trigger event
   *
   * @param s3Event triggered this lambda
   * @return update lambda parameters
   */
  private LambdaParameters setLambdaparameters(S3Event s3Event) {
//    oldKey = s3Event.getRecords().get(0).getS3().getObject().getKey();
//    bucketName = s3Event.getRecords().get(0).getS3().getBucket().getName();

    return LambdaParameters
        .builder()
        .bucketName(bucketName)
        .s3Key(oldKey)
        .stepFunctionId(UUID.randomUUID()).build();
  }

  /**
   * Compare target image with each family member
   * @param parameters lambda parameters
   * @return true if family member is present in image else false
   */
  public boolean isFamilyMemberFound(LambdaParameters parameters) {
    // Target object
    S3Object targetS3Object = new S3Object();
    targetS3Object.setBucket(bucketName);
    targetS3Object.setName(oldKey);

    // List Family Members
    ListObjectsV2Result result = listFamilyMembers();

    if (result.getObjectSummaries() != null && result.getObjectSummaries().size() > 0) {
      // Remove directory file
      result.getObjectSummaries().remove(0);

      // Iterate through family list until member is found or list is empty
      for (S3ObjectSummary summary : result.getObjectSummaries()) {
        // Create source on each iteration with new family member
        S3Object sourceS3Object = new S3Object();
        sourceS3Object.setBucket(summary.getBucketName());
        sourceS3Object.setName(summary.getKey());

        // Compare face in AWSRekognition
        CompareFacesResult compareFacesResult = compareFace(sourceS3Object, targetS3Object);
        if (compareFacesResult != null) {
          List<CompareFacesMatch> facesMatches = compareFacesResult.getFaceMatches();
          for (CompareFacesMatch faceMatch : facesMatches) {
            float confidence = faceMatch.getFace().getConfidence();
            context.getLogger().log("Face confidence : " + confidence);
            System.out.println("Face confidence : " + confidence);
            if (confidence > 95) {
              // Fetch name from s3 key
              String name = summary.getKey().split("/")[1];
              // Remove extension from name
              name = name.split(".")[0];
              // Set family member name  & return result
              parameters.setFamilyMemberName(name);
              // return result
              return true;
            }
          }
        } else {
          // Probably Image having human but not front-facing
          context.getLogger().log("Probably Image having human but not front-facing.");
          return false;
        }
      }
    }
    // return result
    return false;
  }

  /**
   * Copy image to familyVisit folder
   * @param parameters lambda parameters
   * @return updated lambda parameters
   */
  private LambdaParameters copyImageToFamily(LambdaParameters parameters) {
    parameters.setFamilyMemberFound(true);
    newKey = "familyVisit/" + oldKey;
    context.getLogger().log("Family - New key : " + newKey);
    System.out.println("Family - New key : " + newKey);
    CopyObjectRequest copyObjectRequest = new CopyObjectRequest(bucketName, oldKey, bucketName, newKey);
    s3Client.copyObject(copyObjectRequest);
    context.getLogger().log("Object copied to \"familyVisit\" folder.");
    System.out.println("Object copied to \"family_found\" folder.");
    parameters.setS3Key(newKey);
    return parameters;
  }
}
