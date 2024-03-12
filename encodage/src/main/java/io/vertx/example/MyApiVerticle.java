package io.vertx.example;

import io.vertx.example.resource.VideoResource;
import io.vertx.core.AbstractVerticle;
import io.vertx.core.VertxOptions;
import io.vertx.core.logging.Logger;
import io.vertx.core.logging.LoggerFactory;
import io.vertx.example.service.VideoService;
import io.vertx.ext.web.Router;
import ws.schild.jave.EncoderException;

import java.util.List;

public class MyApiVerticle extends AbstractVerticle {
  private static final Logger LOGGER = LoggerFactory.getLogger(MyApiVerticle.class);
  @Override
  public void start() throws Exception {
    LOGGER.info("Dans le start...");
    final Router router = Router.router(vertx);
    final VideoResource videoResource = new VideoResource();
    // LOGGER.info("-------------------------------------");
    // try {
    //   final List<String> formats = videoService.EncodeVideo("http://myapi:5000/static/TextInMotion-VideoSample-720p.mp4", 720);
    //   for (String format : formats) {
    //     LOGGER.info(format);
    //   }

    // }
    // catch (EncoderException e) {
    //   LOGGER.info("+++++++++++++++++++++++++++++++++++++++");
    //   LOGGER.info(e);
    // }
    
    final Router videoSubRouter = videoResource.getSubRouter(vertx);
    router.mountSubRouter("/myapi", videoSubRouter);
    vertx.createHttpServer()
      .requestHandler(router)
      .listen(8080);
  }
  @Override
  public void stop() throws Exception {
    LOGGER.info("Dans le stop...");
  }
}
