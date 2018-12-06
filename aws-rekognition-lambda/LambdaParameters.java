package model;

import lombok.Builder;
import lombok.Data;
import lombok.ToString;

import java.util.UUID;

@Data
@ToString
@Builder
public class LambdaParameters {

  private String s3Key;
  private String bucketName;
  private boolean humanFound;
  private boolean familyMemberFound;
  private String familyMemberName = "";
  private UUID stepFunctionId;

}
