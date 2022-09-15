package com.example.apiinfo.controllers;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

@RestController
@RequestMapping(path = "/api/next")
@CrossOrigin(origins = "http://localhost:4200", allowedHeaders = "*",methods = {RequestMethod.GET})
public class NextArticlesController {

    @Value("${serp.api_key}")
    private String API_KEY;

    Logger logger = LoggerFactory.getLogger(getClass());

    @GetMapping
    public Object getNext(@RequestParam(name = "next") String url, RestTemplate restTemplate){
        String serpUrl = UriComponentsBuilder.fromUriString(url)
                .queryParam("key",API_KEY)
                .toUriString();
        logger.info(url);
        Object obj = restTemplate.getForEntity(serpUrl,Object.class);

        return obj;
    }
}
