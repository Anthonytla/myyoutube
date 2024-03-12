package io.vertx.example.resource;

import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

import com.fasterxml.jackson.databind.ObjectMapper;

import io.vertx.core.Vertx;
import io.vertx.core.json.JsonObject;
import io.vertx.core.logging.Logger;
import io.vertx.core.logging.LoggerFactory;
import io.vertx.example.entity.VideoEncoder;
//import io.vertx.example.entity.VideoFormat;
import io.vertx.example.service.VideoService;
import io.vertx.ext.web.Router;
import io.vertx.ext.web.RoutingContext;
import io.vertx.ext.web.handler.BodyHandler;
import ws.schild.jave.EncoderException;

public class VideoResource{

    private static final Logger LOGGER = LoggerFactory.getLogger(VideoResource.class);


    public Router getSubRouter(final Vertx vertx) {
        final Router subRouter = Router.router(vertx);

        // Body handler
        subRouter.route("/*").handler(BodyHandler.create());

        // Routes
        // subRouter.get("/").handler(this::getAllDogs);
        subRouter.post("/encode").handler(event -> {
            try {
                encoder(event);
            } catch (IOException e) {
                LOGGER.info("IOException"+e.getMessage());
                e.printStackTrace();
            } catch (EncoderException e) {
                // TODO Auto-generated catch block
                LOGGER.info("EncoderException:"+e.getMessage());
                e.printStackTrace();
            } catch (URISyntaxException e) {
                // TODO Auto-generated catch block
                LOGGER.info("URISyntaxException"+e.getMessage());
                e.printStackTrace();
            }
        });

        return subRouter;
    }

    // private void getAllDogs(final RoutingContext routingContext) {
    // LOGGER.info("Dans getAllDogs...");

    // final List<Dog> dogs = dogService.findAll();

    // final JsonObject jsonResponse = new JsonObject();
    // jsonResponse.put("dogs", dogs);
    // jsonResponse.put("my-name", "Thierry");

    // routingContext.response().setStatusCode(200).putHeader("content-type",
    // "application/json")
    // .end(Json.encode(jsonResponse));
    // }

    private void encoder(final RoutingContext routingContext) throws IOException, EncoderException, URISyntaxException {
        //LOGGER.info("Dans getOneDog...");
        VideoEncoder videoEncoder = new VideoEncoder(routingContext);
        videoEncoder.start();

        /*final JsonObject body = routingContext.getBodyAsJson();
        final Integer id = Integer.parseInt(body.getString("video_id"));
        final String sourcePath = body.getString("source");
        final Integer format = Integer.parseInt(body.getString("format"));
       // VideoFormat video_format = new VideoFormat(body.getString("format"), sourcePath, id);
        StringBuilder fullSourcePath = new StringBuilder("http://localhost:5000");
        fullSourcePath.append(sourcePath);
        LOGGER.info(fullSourcePath.toString());
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
            LOGGER.info("format:" + height);
            if (height >= format) {
                continue;
            }
           // video_format.setCode(height.toString());
            final VideoService videoService = new VideoService(fullSourcePath.toString() ,height);
            videoService.run();
            dones.add(height);
            LOGGER.info(dones.toString());
            //video_format.setUri(path);
            //apiCall(video_format);

        }*/

    }

    /*private void apiCall(VideoFormat video_format) {
        try{
            URL url = new URL("http://localhost:5000/myapi/format/"+video_format.getVideoId());
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setDoOutput(true);
            LOGGER.info("url:"+url.getPath());
            connection.setRequestMethod("PUT");
            

            
            //connection.setDoOutput(true);
            //connection.setRequestProperty("Content-Type", "application/json");

            final ObjectMapper mapper = new ObjectMapper();
            final String data = mapper.writeValueAsString(video_format);

            LOGGER.info(data);


            //String data = "{\n  \"code\":  ,\n  \"Customer\": \"John Smith\",\n  \"Quantity\": 1,\n  \"Price\": 10.00\n}";

            byte[] out = data.getBytes(StandardCharsets.UTF_8);

            OutputStream stream = connection.getOutputStream();
            stream.write(out);

            int status = connection.getResponseCode();
            LOGGER.info("status:"+status);
            //LOGGER.info("Before disconnect"+connection.getResponseCode() + " " + connection.getResponseMessage());
            connection.disconnect();

        }
        catch(MalformedURLException e) {
            LOGGER.info(e.getMessage());
        }
        catch(IOException e) {
            LOGGER.info(e.getMessage());
        }
    }*/
}