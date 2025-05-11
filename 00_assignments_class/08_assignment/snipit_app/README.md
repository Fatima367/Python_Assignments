# Snipit

A personal space to save and organize notes, along with generating AI-powered cheat codes for multiple categories.

## Project Overview

This Notes App is a Streamlit-based web application that provides users with a personal space to create, manage, and organize their notes. Additionally, it features an AI-powered "Cheat Codes" generator that can create quick reference guides for various categories like Math and Programming.


## Features

- **User Authentication**: Secure login system to protect user data
- **Notes Management**: Create, read, update, and delete personal notes
- **Note Organization**: Star important notes for quick access
- **Cheat Codes Generator**: AI-powered generation of quick reference guides for:
  - Math formulas and concepts
  - Programming syntax and snippets
  - And more categories
- **Responsive UI**: Clean and intuitive user interface with color-coded notes

## Object-Oriented Programming Implementation

The application is built using Object-Oriented Programming principles:

### Classes and Objects

1. **Notes Class**
   - Implements static methods for note management
   - Handles CRUD operations (Create, Read, Update, Delete)
   - Example methods:
     - `create_note()`
     - `get_user_notes()`
     - `update_note()`
     - `delete_note()`
     - `is_starred()`

2. **Login Class** (implied in the code)
   - Handles user authentication
   - Manages user sessions

# OOP Principles Applied

## 1. **Encapsulation**
   - Data and methods are encapsulated within the Notes class
   - Note properties (title, content, about, etc.) are bundled together
   - Implementation details are hidden from the user interface

## 2. **Abstraction**
   - Complex operations like note creation and retrieval are abstracted into simple method calls
   - Users interact with high-level functions without needing to understand the underlying implementation

## 3. **Inheritance** (implied in the structure)
   - Different note types (regular notes and cheat codes) share common properties and behaviors

## 4. **Polymorphism**
   - The `get_user_notes()` method can filter notes based on type parameter
   - Same methods handle different types of notes (regular notes vs. cheat codes)

## Benefits of OOP in This Project

The Object-Oriented approach provides several advantages for this Notes App:

1. **Modularity**: The application is divided into logical components (Notes, Login, UI rendering) that can be developed, tested, and maintained independently.

2. **Reusability**: Common functionality like CRUD operations are implemented once in the Notes class and reused throughout the application.

3. **Maintainability**: Changes to one part of the system (e.g., how notes are stored) can be made without affecting other parts (e.g., the UI).

4. **Scalability**: New features can be added by extending existing classes or creating new ones without rewriting existing code. For example, adding new note types or categories.

5. **Organization**: The code is well-structured and organized around real-world entities (notes, users), making it easier to understand and navigate.

6. **Readability**: The code is more intuitive as it models real-world objects and their interactions.

7. **Data Security**: Encapsulation helps protect data integrity by controlling how note data is accessed and modified.


## Code Structure

The application follows a modular structure:

- **Main Application Logic**: Handles routing and page rendering
- **Class Definitions**: Implements OOP principles for data management
- **UI Components**: Renders different pages and UI elements
- **State Management**: Uses Streamlit's session state for maintaining application state