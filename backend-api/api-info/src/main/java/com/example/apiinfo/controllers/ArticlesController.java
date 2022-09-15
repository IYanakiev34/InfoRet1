package com.example.apiinfo.controllers;



import com.google.gson.JsonObject;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@RestController
@RequestMapping(path= "/api/articles")
@CrossOrigin(origins = "http://localhost:4200",allowedHeaders = "*",methods = {RequestMethod.GET,RequestMethod.POST})
public class ArticlesController {

    @Value("${serp.api_key}")
    private String API_KEY;

    Logger logger = LoggerFactory.getLogger(getClass());



    @GetMapping
    public Object getArticles(@RequestParam(name="author") String authorId
            , @RequestParam(name="sort") String sorting
            , RestTemplate restTemplate){
        

        String url = UriComponentsBuilder.fromUriString("https://serpapi.com/search.json")
                .queryParam("api_key",API_KEY)
                .queryParam("sort",sorting)
                .queryParam("author_id",authorId)
                .queryParam("engine","google_scholar_author")
                .queryParam("start",0)
                .queryParam("num",100)
                .toUriString();

        Object object = restTemplate.getForEntity(url,Object.class);
        return object;
    }
}
