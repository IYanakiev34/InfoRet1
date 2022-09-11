package com.example.apiinfo.controllers;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;


@RestController
@RequestMapping(path = "/api/author")
@CrossOrigin(origins = "http://localhost:4200", allowedHeaders = "*",methods = {RequestMethod.GET,RequestMethod.POST})
public class AuthorsController {
    Logger logger = LoggerFactory.getLogger(getClass());
    @Value("${serp.api_key}")
    private String API_KEY;


    @GetMapping
    public Object getAuthor(@RequestParam(name="name") String name, RestTemplate restTemplate){
        String url = UriComponentsBuilder.fromUriString("https://serpapi.com/search.json")
                .queryParam("engine","google_scholar_profiles")
                .queryParam("mauthors", name)
                .queryParam("api_key", API_KEY)
                .toUriString();

        Object obj = restTemplate.getForEntity(url,Object.class);

        return obj;
    }
}

