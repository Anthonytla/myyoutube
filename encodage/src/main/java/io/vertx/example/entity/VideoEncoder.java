package io.vertx.example.entity;

import java.io.IOException;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.vertx.core.json.JsonObject;
import io.vertx.core.logging.Logger;
import io.vertx.core.logging.LoggerFactory;
import io.vertx.example.service.VideoService;
import io.vertx.ext.web.RoutingContext;

public class VideoEncoder extends Thread {
    private RoutingContext routingContext;
    private static final Logger LOGGER = LoggerFactory.getLogger(VideoEncoder.class);
    public VideoEncoder(RoutingContext routingContext) {
        super();
        this.routingContext = routingContext;
    }
    public void run() {
        final JsonObject body = routingContext.getBodyAsJson();
        final Integer id = Integer.parseInt(body.getString("video_id"));
        final String sourcePath = body.getString("source");
        final Integer format = Integer.parseInt(body.getString("format"));
        final String user_mail = body.getString("email");
        VideoFormat video_format = new VideoFormat(body.getString("format"), sourcePath, id);
        StringBuilder fullSourcePath = new StringBuilder("http://myapi:5000");
        fullSourcePath.append(sourcePath);
        //LOGGER.info(fullSourcePath.toString());
        JsonObject json = new JsonObject()
                .put("message", "OOK");
        routingContext.response().setStatusCode(200).putHeader("content-type", "application/json").end(json.encodePrettily());
        
        List<Integer> res = new ArrayList<>();
        res.add(1080);
        res.add(720);
        res.add(480);
        res.add(360);
        res.add(240);
        res.add(144);

        List<Integer> dones = new ArrayList<>();
        for (Integer height : res) {
           // LOGGER.info("format:" + height);
            if (height > format) {
                continue;
            }
            video_format.setCode(height.toString());
            final VideoService videoService = new VideoService(fullSourcePath.toString() ,height);
            String path = videoService.run();
            dones.add(height);
            LOGGER.info(dones.toString());
            // LOGGER.info("PATH"+path);
            video_format.setUri(path);
            updateFormat(video_format);

        }
        sendMail(user_mail);
    }
    private void updateFormat(VideoFormat video_format) {
        try {
            URL url = new URL("http://myapi:5000/myapi/format/" + video_format.getVideoId());
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
           // LOGGER.info("url:" + url.getPath());
            connection.setRequestMethod("PUT");

            // connection.setDoOutput(true);
            // connection.setRequestProperty("Content-Type", "application/json");

            final ObjectMapper mapper = new ObjectMapper();
            final String data = mapper.writeValueAsString(video_format);

            //LOGGER.info(data);

            // String data = "{\n \"code\": ,\n \"Customer\": \"John Smith\",\n
            // \"Quantity\": 1,\n \"Price\": 10.00\n}";

           // byte[] out = data.getBytes(StandardCharsets.UTF_8);

            OutputStreamWriter outs = new OutputStreamWriter(connection.getOutputStream());
            outs.write(data);
            outs.close();
            //LOGGER.info(outs.toString());

            int status = connection.getResponseCode();
            //LOGGER.info("status:" + status);
            // LOGGER.info("Before disconnect"+connection.getResponseCode() + " " +
            // connection.getResponseMessage());
            connection.disconnect();

        } catch (MalformedURLException e) {
            LOGGER.info(e.getMessage());
        } catch (IOException e) {
            LOGGER.info(e.getMessage());
        }
    }
    private void sendMail(final String user_mail) {
        try {
            URL url = new URL("http://mailing:8082/mail/" + user_mail + "/1");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            //LOGGER.info("url:" + url.getPath());
            connection.setRequestMethod("GET");
            int status = connection.getResponseCode();
            //LOGGER.info("status:" + status);
            // LOGGER.info("Before disconnect"+connection.getResponseCode() + " " +
            // connection.getResponseMessage());
            connection.disconnect();

        }catch (MalformedURLException e) {
            LOGGER.info(e.getMessage());
        } catch (IOException e) {
            LOGGER.info(e.getMessage());
        }
    }
}
