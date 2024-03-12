package io.vertx.example.entity;

public class VideoFormat {
    private String code;
    private String uri;
    private Integer video_id;
    public VideoFormat(String code, String uri, Integer video_id) {
        super();
        this.code = code;
        this.uri = uri;
        this.video_id = video_id;
    };

    public String getCode() {
        return this.code;
    }

    public String getUri() {
        return this.uri;    
    }

    public Integer getVideoId() {
        return this.video_id;
    }

    public VideoFormat setCode(String code) {
        this.code = code;
        return this;
    }

    public VideoFormat setUri(String uri) {
        this.uri = uri;
        return this;
    }
}
