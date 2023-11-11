package com.example.demo;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

@RestController
public class HelloWorldController {

    @GetMapping("/g")
    public String greeting() {
        return "Greetings from Spring Boot!";
    }

    @GetMapping("/")
    public void login_page() throws IOException {
        ProcessBuilder processBuilder = new ProcessBuilder("python", "login_page.py");
        processBuilder.redirectErrorStream(true);
        Process process = processBuilder.start();
//        BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));
//        String pyString = input.readLine();
//        return pyString;
    }

}