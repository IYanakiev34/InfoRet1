package com.example.apiinfo.controllers;



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


    @GetMapping
    public Object getArticles(@RequestParam(name="author") String authorId
            , @RequestParam(name="sort") String sorting
            , @RequestParam(name="start", required = false)int start
            , @RequestParam(name="num", required = false) int num
            , RestTemplate restTemplate){
        

        String url = UriComponentsBuilder.fromUriString("https://serpapi.com/search.json")
                .queryParam("api_key",API_KEY)
                .queryParam("sort",sorting)
                .queryParam("author_id",authorId)
                .queryParam("engine","google_scholar_author")
                .queryParam("start",start)
                .queryParam("num", num)
                .toUriString();

        // TODO: convert to JsonObject and send it back
        // TODO: add Gson dependency to convert it ot JSON object
        Object obj =  restTemplate.getForEntity(url,Object.class);

        return obj;
    }
}
