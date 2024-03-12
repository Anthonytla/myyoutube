package io.vertx.example.service;

import java.io.*;
import java.net.MalformedURLException;
import java.net.URI;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

import io.vertx.example.MyApiVerticle;
import org.apache.commons.io.FileUtils;
import org.apache.commons.io.FilenameUtils;
import ws.schild.jave.Encoder;
import ws.schild.jave.EncoderException;
import ws.schild.jave.InputFormatException;
import ws.schild.jave.MultimediaObject;
import io.vertx.core.logging.Logger;
import io.vertx.core.logging.LoggerFactory;
import ws.schild.jave.encode.AudioAttributes;
import ws.schild.jave.encode.EncodingAttributes;
import ws.schild.jave.encode.VideoAttributes;
import ws.schild.jave.encode.enums.X264_PROFILE;
import ws.schild.jave.info.VideoSize;


public class VideoService{
  private String sourcePath;
  private Integer format;
  public VideoService(String sourcePath, Integer format) {
    super();
    this.sourcePath = sourcePath;
    this.format = format;
  }

  private static final Logger LOGGER = LoggerFactory.getLogger(VideoService.class);

  public String run() {
    URL url;
  try {
      url = new URL(this.sourcePath);
    
      InputStream source = url.openStream();
     
      //File sourceFile = new File("static/"+"copy"+FilenameUtils.getName(url.getPath()));
      File sourceFile = new File("static/"+"copy"+FilenameUtils.getName(url.getPath()));
      FileUtils.copyInputStreamToFile(source, sourceFile);
    /*
     * List<Integer> res = new ArrayList<>(); res.add(1080); res.add(720);
     * res.add(480); res.add(360); res.add(240); res.add(144); List<String> formats
     * = new ArrayList<>();
     */
    // for (Integer height : res) {
    // if (height >= format) { continue; }
    File target = new File("static/"+this.format+"/"+FilenameUtils.getName(url.getPath()));
    //LOGGER.info("sourceFile:"+sourceFile.toString());
    //if (target.exists()) {LOGGER.info(target.getAbsolutePath());}
    
    AudioAttributes audio = new AudioAttributes();
    audio.setCodec("aac");
    audio.setBitRate(64000);
    audio.setChannels(2);
    audio.setSamplingRate(44100);
    VideoAttributes video = new VideoAttributes();
    video.setCodec("h264");
    video.setX264Profile(X264_PROFILE.BASELINE);
    video.setBitRate(1600000);
    // More the frames more quality and size, but keep it low based on devices like
    // mobile
    video.setFrameRate(25);
    //video.setSize(new VideoSize(this.format, 1280));
    if (this.format == 1080) { video.setSize(VideoSize.hd1080);}
    if (this.format == 480) { video.setSize(VideoSize.hd480); }
    if (this.format == 720) { video.setSize(VideoSize.hd720); }
    if (this.format == 360) { video.setSize(new VideoSize(640, 360)); }
    if (this.format == 240) { video.setSize(new VideoSize(426, 240)); }
    if (this.format == 144) { video.setSize(new VideoSize(256, 144)); }
    EncodingAttributes attrs = new EncodingAttributes();
    // attrs.setOutputFormat("3gp");
    // attrs.setAudioAttributes(audio);
    attrs.setVideoAttributes(video);
    Encoder encoder = new Encoder();
    encoder.encode(new MultimediaObject(sourceFile), target, attrs);
    //String targetBaseName = FilenameUtils.getBaseName(target.getName());
    StringBuilder targetFullPath = new StringBuilder("static/"+this.format+"/"+FilenameUtils.getName(url.getPath()));
    
    sourceFile.delete();
    return targetFullPath.toString();
    }
    catch (IOException e) {
      LOGGER.info("IOException"+e.getMessage());
      return null;

    }
    catch(InputFormatException e) {
      LOGGER.info("InputFormatException"+e.getMessage());
      return null;
    }
    catch(EncoderException e) {
      LOGGER.info("EncoderException"+e.getMessage());
      return null;
    }
   
    // formats.add(height.toString());
    // }
    
  }

  public File whenConvertingInputStreamToFile_thenCorrect4(InputStream stream) throws IOException {
    File targetFile = new File("targetFile.tmp");
    FileUtils.copyInputStreamToFile(stream, targetFile);
    return targetFile;
  }
}
