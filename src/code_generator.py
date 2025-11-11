"""
Code Generation Module for Pseudo Code and Source Code
Supports Java and Angular
"""
from typing import List, Dict
from .models import JiraIssue, PseudoCode, SourceCode, ComplexityLevel


class PseudoCodeGenerator:
    """Generates pseudo code from Jira issue analysis"""
    
    def __init__(self, language: str):
        self.language = language
    
    def generate(self, issue: JiraIssue) -> PseudoCode:
        """Generate pseudo code based on issue details"""
        
        # Analyze complexity
        complexity = self._analyze_complexity(issue)
        
        # Generate sections based on issue type
        sections = self._generate_sections(issue)
        
        # Add notes
        notes = self._generate_notes(issue, complexity)
        
        return PseudoCode(
            sections=sections,
            complexity=complexity,
            notes=notes
        )
    
    def _analyze_complexity(self, issue: JiraIssue) -> ComplexityLevel:
        """Analyze issue complexity based on type and description"""
        issue_type = issue.issue_type.lower()
        description_length = len(issue.description)
        
        # Simple heuristic - can be enhanced with AI
        if issue_type in ["bug", "task"] and description_length < 200:
            return ComplexityLevel.SIMPLE
        elif issue_type in ["feature", "story"] or description_length > 500:
            return ComplexityLevel.COMPLEX
        else:
            return ComplexityLevel.MODERATE
    
    def _generate_sections(self, issue: JiraIssue) -> List[Dict[str, str]]:
        """Generate pseudo code as a single BEGIN/END block"""
        # Generate all pseudo code steps in a single block
        all_steps = self._get_complete_pseudo_code(issue)
        
        sections = [{
            "title": "Implementation Algorithm",
            "steps": all_steps
        }]
        
        return sections
    
    def _get_complete_pseudo_code(self, issue: JiraIssue) -> str:
        """Generate complete pseudo code in a single BEGIN/END block based on issue description"""
        
        # Extract key requirements from description
        description = issue.description.lower()
        title = issue.title.lower()
        
        # Analyze what needs to be done based on description
        is_crud = any(word in description or word in title for word in ['create', 'update', 'delete', 'fetch', 'get', 'list', 'save'])
        has_validation = any(word in description for word in ['validate', 'check', 'verify', 'required', 'mandatory'])
        has_api = any(word in description for word in ['api', 'endpoint', 'service', 'rest', 'http'])
        has_db = any(word in description for word in ['database', 'table', 'repository', 'store', 'persist', 'query'])
        has_auth = any(word in description for word in ['auth', 'login', 'permission', 'access', 'role', 'user'])
        
        if self.language == "java":
            return self._generate_java_pseudo_code(issue, is_crud, has_validation, has_api, has_db, has_auth)
        else:  # angular
            return self._generate_angular_pseudo_code(issue, is_crud, has_validation, has_api, has_db, has_auth)
    
    def _generate_java_pseudo_code(self, issue: JiraIssue, is_crud: bool, has_validation: bool, 
                                   has_api: bool, has_db: bool, has_auth: bool) -> str:
        """Generate Java-specific pseudo code based on requirements"""
        steps = ["BEGIN"]
        
        # Add authentication check if needed
        if has_auth:
            steps.append("  // Authentication & Authorization")
            steps.append("  VERIFY user authentication token")
            steps.append("  CHECK user permissions for this operation")
            steps.append("  IF unauthorized THEN")
            steps.append("    RETURN 401/403 error response")
            steps.append("  END IF")
            steps.append("")
        
        # Add input validation
        if has_validation or is_crud:
            steps.append("  // Input Validation")
            steps.append(f"  // Based on requirement: {issue.title}")
            steps.append("  VALIDATE incoming request parameters")
            steps.append("    CHECK required fields from description:")
            # Extract requirements from description
            for line in issue.description.split('\n')[:5]:  # First 5 lines
                if line.strip():
                    steps.append(f"    //   - {line.strip()[:60]}")
            steps.append("  IF validation fails THEN")
            steps.append("    THROW ValidationException")
            steps.append("  END IF")
            steps.append("")
        
        # Add main business logic
        steps.append("  // Main Business Logic")
        steps.append(f"  // Implementing: {issue.title}")
        
        if is_crud:
            if 'create' in issue.title.lower() or 'save' in issue.title.lower():
                steps.append("  CREATE new entity from request data")
                if has_db:
                    steps.append("  SAVE entity to database")
            elif 'update' in issue.title.lower():
                steps.append("  FETCH existing entity by ID")
                steps.append("  UPDATE entity fields with new values")
                if has_db:
                    steps.append("  SAVE updated entity to database")
            elif 'delete' in issue.title.lower():
                steps.append("  FETCH entity by ID")
                steps.append("  PERFORM soft/hard delete")
                if has_db:
                    steps.append("  REMOVE from database")
            elif 'get' in issue.title.lower() or 'fetch' in issue.title.lower() or 'list' in issue.title.lower():
                steps.append("  QUERY database with filters")
                steps.append("  FETCH matching records")
                steps.append("  APPLY pagination if needed")
        else:
            steps.append(f"  PROCESS request according to: {issue.description[:100]}")
            steps.append("  APPLY business rules and transformations")
        
        if has_db:
            steps.append("  EXECUTE database transaction")
        
        steps.append("")
        
        # Add response generation
        steps.append("  // Response Generation")
        steps.append("  CREATE response DTO")
        steps.append("  SET success status")
        steps.append("  POPULATE response data")
        steps.append("  RETURN ResponseEntity with HTTP status")
        steps.append("")
        
        # Add error handling
        steps.append("  // Error Handling")
        steps.append("  ON ValidationException")
        steps.append("    LOG error details")
        steps.append("    RETURN 400 Bad Request")
        if has_db:
            steps.append("  ON DataNotFoundException")
            steps.append("    RETURN 404 Not Found")
            steps.append("  ON SQLException")
            steps.append("    ROLLBACK transaction")
            steps.append("    RETURN 500 Internal Server Error")
        steps.append("  ON Exception")
        steps.append("    LOG error with context")
        steps.append("    RETURN 500 error response")
        steps.append("END")
        
        return "\n".join(steps)
    
    def _generate_angular_pseudo_code(self, issue: JiraIssue, is_crud: bool, has_validation: bool,
                                      has_api: bool, has_db: bool, has_auth: bool) -> str:
        """Generate Angular-specific pseudo code based on requirements"""
        steps = ["BEGIN"]
        
        # Component initialization
        steps.append("  // Component Initialization")
        steps.append(f"  // For feature: {issue.title}")
        steps.append("  INITIALIZE component variables")
        
        if is_crud:
            steps.append("  DECLARE data model interface")
            if 'list' in issue.title.lower() or 'get' in issue.title.lower():
                steps.append("  DECLARE array to hold list data")
        
        steps.append("")
        
        # Form setup if validation needed
        if has_validation or 'form' in issue.description.lower():
            steps.append("  // Form Setup")
            steps.append("  CREATE FormGroup with FormControls")
            steps.append("    Based on requirements:")
            for line in issue.description.split('\n')[:5]:
                if line.strip():
                    steps.append(f"    //   - {line.strip()[:60]}")
            steps.append("  ADD validators (required, pattern, custom)")
            steps.append("")
        
        # Data loading
        if 'list' in issue.title.lower() or 'display' in issue.title.lower() or 'show' in issue.title.lower():
            steps.append("  // Data Loading (ngOnInit)")
            steps.append("  SHOW loading indicator")
            steps.append("  CALL service to fetch data")
            steps.append("  SUBSCRIBE to observable")
            steps.append("    ON success:")
            steps.append("      STORE data in component variable")
            steps.append("      UPDATE UI table/list")
            steps.append("      HIDE loading indicator")
            steps.append("    ON error:")
            steps.append("      DISPLAY error message")
            steps.append("      HIDE loading indicator")
            steps.append("")
        
        # Main action (submit, save, etc.)
        steps.append("  // Main Action Handler")
        steps.append(f"  // Implementing: {issue.title}")
        
        if has_validation:
            steps.append("  ON user action (click/submit)")
            steps.append("    CHECK form validity")
            steps.append("    IF invalid THEN")
            steps.append("      DISPLAY validation errors")
            steps.append("      RETURN")
            steps.append("    END IF")
            steps.append("")
        
        if has_api:
            steps.append("    SHOW loading spinner")
            steps.append("    PREPARE request payload from form")
            steps.append("    CALL API service method")
            steps.append("      ON success response:")
            steps.append("        UPDATE local state")
            steps.append("        DISPLAY success notification")
            steps.append("        RESET form OR navigate to list")
            steps.append("      ON error response:")
            steps.append("        PARSE error message")
            steps.append("        DISPLAY error notification")
            steps.append("    HIDE loading spinner")
        
        steps.append("")
        steps.append("  // Error Handling")
        steps.append("  CATCH HTTP errors")
        steps.append("  LOG errors to console")
        steps.append("  SHOW user-friendly messages")
        steps.append("END")
        
        return "\n".join(steps)

    def _get_input_validation_steps(self, issue: JiraIssue) -> str:
        """Generate input validation pseudo code"""
        if self.language == "java":
            return """BEGIN
  VALIDATE incoming request parameters
    CHECK if required fields are present
    VERIFY data types match expected format
    SANITIZE input to prevent injection attacks
  IF validation fails THEN
    THROW ValidationException with error details
  END IF
  LOG validation success
END""".strip()
        else:  # angular
            return """BEGIN
  CREATE FormGroup with validation rules
    SET required validators on mandatory fields
    ADD custom validators for business rules
    BIND form to component
  SUBSCRIBE to form value changes
    UPDATE validation messages
    ENABLE/DISABLE submit button based on validity
  ON form submit
    CHECK form.valid status
    IF invalid THEN
      DISPLAY error messages
      RETURN
    END IF
END""".strip()
    
    def _get_main_logic_steps(self, issue: JiraIssue) -> str:
        """Generate main logic pseudo code"""
        if self.language == "java":
            return f"""BEGIN
  INITIALIZE service layer components
  BEGIN transaction
    FETCH existing data from database/repository
    APPLY business logic transformation
      {self._get_business_logic_hint(issue)}
    VALIDATE business rules
    UPDATE/INSERT data into database
  COMMIT transaction
  RETURN success response with generated IDs
END""".strip()
        else:  # angular
            return f"""BEGIN
  SHOW loading spinner
  CALL backend API service method
    PASS validated form data
    SET appropriate HTTP headers
  ON successful response
    UPDATE component state with response data
    REFRESH data grid/list if needed
    {self._get_ui_update_hint(issue)}
  HIDE loading spinner
  DISPLAY success notification
END""".strip()
    
    def _get_business_logic_hint(self, issue: JiraIssue) -> str:
        """Get business logic hint from issue"""
        if "calculate" in issue.description.lower():
            return "CALCULATE values based on input parameters"
        elif "validate" in issue.description.lower():
            return "VALIDATE data against business rules"
        elif "transform" in issue.description.lower():
            return "TRANSFORM data to required format"
        else:
            return "PROCESS data according to requirements"
    
    def _get_ui_update_hint(self, issue: JiraIssue) -> str:
        """Get UI update hint from issue"""
        if "table" in issue.description.lower() or "grid" in issue.description.lower():
            return "REFRESH data table/grid"
        elif "form" in issue.description.lower():
            return "RESET form to initial state"
        else:
            return "UPDATE UI components with new data"
    
    def _get_error_handling_steps(self) -> str:
        """Generate error handling pseudo code"""
        if self.language == "java":
            return """BEGIN
  TRY
    // All operations here
  CATCH ValidationException
    LOG error with context
    RETURN 400 Bad Request with error details
  CATCH DataNotFoundException
    LOG warning
    RETURN 404 Not Found
  CATCH SQLException/DataAccessException
    LOG error with stack trace
    ROLLBACK transaction
    RETURN 500 Internal Server Error
  CATCH Exception
    LOG error with full context
    RETURN 500 with generic error message
  END TRY-CATCH
END""".strip()
        else:  # angular
            return """BEGIN
  IMPLEMENT error interceptor
  ON HTTP error response
    PARSE error details from response body
    MAP error code to user-friendly message
    DISPLAY error notification/toast
    IF error code = 401 (Unauthorized) THEN
      REDIRECT to login page
    ELSE IF error code = 403 (Forbidden) THEN
      SHOW access denied message
    ELSE IF error code = 500 (Internal Server Error) THEN
      LOG error to console
      SHOW generic error message
    END IF
  HIDE loading indicators
END""".strip()
    
    def _get_output_steps(self, issue: JiraIssue) -> str:
        """Generate output generation pseudo code"""
        if self.language == "java":
            return """BEGIN
  CREATE response DTO object
  SET success flag to true
  SET response message
  POPULATE data fields from result
  ADD metadata (timestamp, request ID)
  RETURN ResponseEntity with HTTP 200/201
  LOG successful operation
END""".strip()
        else:  # angular
            return """BEGIN
  UPDATE component properties with response data
  TRIGGER change detection
  EMIT events to parent components if needed
  UPDATE routing if navigation required
  SAVE state to local storage/session storage if needed
  LOG successful operation to analytics
END""".strip()
    
    def _generate_notes(self, issue: JiraIssue, complexity: ComplexityLevel) -> List[str]:
        """Generate implementation notes"""
        notes = [
            f"Complexity Level: {complexity.value}",
            f"Target Language: {self.language.upper()}",
        ]
        
        if complexity == ComplexityLevel.COMPLEX:
            notes.append("Consider breaking down into smaller components/services")
            notes.append("Add comprehensive unit tests for each component")
        
        if self.language == "java":
            notes.extend([
                "Use Spring Boot best practices",
                "Implement proper dependency injection",
                "Add logging using SLF4J"
            ])
        else:
            notes.extend([
                "Follow Angular style guide",
                "Use RxJS operators for async operations",
                "Implement OnDestroy for cleanup"
            ])
        
        return notes


class SourceCodeGenerator:
    """Generates source code from pseudo code"""
    
    def __init__(self, language: str):
        self.language = language
    
    def generate(self, issue: JiraIssue, pseudo_code: PseudoCode) -> SourceCode:
        """
        Generate source code based on Jira issue description and pseudo code
        
        Uses issue title and description to determine:
        - Class/component names
        - Entity fields
        - API endpoints
        - Business logic structure
        """
        
        if self.language == "java":
            return self._generate_java_code(issue, pseudo_code)
        else:  # angular
            return self._generate_angular_code(issue, pseudo_code)
    
    def _generate_java_code(self, issue: JiraIssue, pseudo_code: PseudoCode) -> SourceCode:
        """Generate Java/Spring Boot code"""
        
        class_name = self._to_class_name(issue.title)
        
        files = []
        
        # 1. Controller
        files.append({
            "filename": f"{class_name}Controller.java",
            "description": "REST API Controller",
            "code": self._generate_java_controller(class_name)
        })
        
        # 2. Service
        files.append({
            "filename": f"{class_name}Service.java",
            "description": "Business Logic Service",
            "code": self._generate_java_service(class_name)
        })
        
        # 3. Repository
        files.append({
            "filename": f"{class_name}Repository.java",
            "description": "Data Access Layer",
            "code": self._generate_java_repository(class_name)
        })
        
        # 4. DTO
        files.append({
            "filename": f"{class_name}DTO.java",
            "description": "Data Transfer Object",
            "code": self._generate_java_dto(class_name)
        })
        
        # 5. Entity
        files.append({
            "filename": f"{class_name}Entity.java",
            "description": "JPA Entity",
            "code": self._generate_java_entity(class_name)
        })
        
        dependencies = [
            "spring-boot-starter-web",
            "spring-boot-starter-data-jpa",
            "spring-boot-starter-validation",
            "lombok",
            "mapstruct"
        ]
        
        setup_instructions = [
            "Add dependencies to pom.xml or build.gradle",
            "Configure database connection in application.properties",
            "Run database migrations if needed",
            "Build project: mvn clean install",
            "Run application: mvn spring-boot:run"
        ]
        
        return SourceCode(
            language="java",
            files=files,
            dependencies=dependencies,
            setup_instructions=setup_instructions
        )
    
    def _generate_angular_code(self, issue: JiraIssue, pseudo_code: PseudoCode) -> SourceCode:
        """Generate Angular code"""
        
        component_name = self._to_kebab_case(issue.title)
        class_name = self._to_class_name(issue.title)
        
        files = []
        
        # 1. Component TypeScript
        files.append({
            "filename": f"{component_name}.component.ts",
            "description": "Angular Component",
            "code": self._generate_angular_component(class_name)
        })
        
        # 2. Component HTML
        files.append({
            "filename": f"{component_name}.component.html",
            "description": "Component Template",
            "code": self._generate_angular_template(class_name)
        })
        
        # 3. Component CSS
        files.append({
            "filename": f"{component_name}.component.scss",
            "description": "Component Styles",
            "code": self._generate_angular_styles()
        })
        
        # 4. Service
        files.append({
            "filename": f"{component_name}.service.ts",
            "description": "Angular Service for API calls",
            "code": self._generate_angular_service(class_name)
        })
        
        # 5. Model
        files.append({
            "filename": f"{component_name}.model.ts",
            "description": "TypeScript Interface/Model",
            "code": self._generate_angular_model(class_name)
        })
        
        dependencies = [
            "@angular/core",
            "@angular/common",
            "@angular/forms",
            "@angular/router",
            "rxjs"
        ]
        
        setup_instructions = [
            "Add dependencies to package.json",
            "Run: npm install",
            "Import component in module",
            "Add route configuration if needed",
            "Run: ng serve"
        ]
        
        return SourceCode(
            language="angular",
            files=files,
            dependencies=dependencies,
            setup_instructions=setup_instructions
        )
    
    def _to_class_name(self, title: str) -> str:
        """
        Extract key words from title and create concise PascalCase class name
        Example: "Write a wrapper for below mention api" -> "ApiWrapper"
        """
        # Common words to skip
        skip_words = {
            'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'may', 'might', 'must', 'can', 'to', 'of', 'in', 'on', 'at',
            'by', 'for', 'with', 'from', 'as', 'into', 'through', 'during', 'before',
            'after', 'above', 'below', 'between', 'under', 'again', 'further', 'then',
            'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'both',
            'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 'write',
            'create', 'update', 'delete', 'add', 'remove', 'get', 'fetch', 'make',
            'new', 'this', 'that', 'these', 'those', 'mention', 'below', 'above'
        }
        
        # Extract meaningful words
        words = title.replace("-", " ").replace("_", " ").split()
        meaningful_words = []
        
        for word in words:
            clean_word = ''.join(c for c in word if c.isalnum()).lower()
            if clean_word and clean_word not in skip_words and len(clean_word) > 2:
                meaningful_words.append(clean_word.capitalize())
        
        # If we have meaningful words, use them (limit to 3 words for conciseness)
        if meaningful_words:
            # Take max 3 most important words
            if len(meaningful_words) > 3:
                # Prioritize nouns (usually longer words) and keep last word
                meaningful_words = meaningful_words[-3:]
            return "".join(meaningful_words)
        
        # Fallback: use first 3 words from original title
        words = [w.capitalize() for w in words if w.isalnum()][:3]
        return "".join(words) if words else "Default"
    
    def _to_kebab_case(self, title: str) -> str:
        """Convert title to kebab-case"""
        import re
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1-\2', title)
        return re.sub('([a-z0-9])([A-Z])', r'\1-\2', s1).lower().replace(" ", "-")
    
    def _generate_java_controller(self, class_name: str) -> str:
        """Generate Java Spring Controller code"""
        return f'''package com.example.controller;

import com.example.dto.{class_name}DTO;
import com.example.service.{class_name}Service;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import javax.validation.Valid;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("/api/{class_name.lower()}")
@RequiredArgsConstructor
@Validated
public class {class_name}Controller {{

    private final {class_name}Service service;

    @PostMapping
    public ResponseEntity<{class_name}DTO> create(@Valid @RequestBody {class_name}DTO dto) {{
        log.info("Creating new {class_name}: {{}}", dto);
        {class_name}DTO created = service.create(dto);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }}

    @GetMapping("/{id}")
    public ResponseEntity<{class_name}DTO> getById(@PathVariable Long id) {{
        log.info("Fetching {class_name} with id: {{}}", id);
        {class_name}DTO dto = service.findById(id);
        return ResponseEntity.ok(dto);
    }}

    @GetMapping
    public ResponseEntity<List<{class_name}DTO>> getAll() {{
        log.info("Fetching all {class_name}s");
        List<{class_name}DTO> dtos = service.findAll();
        return ResponseEntity.ok(dtos);
    }}

    @PutMapping("/{id}")
    public ResponseEntity<{class_name}DTO> update(@PathVariable Long id, @Valid @RequestBody {class_name}DTO dto) {{
        log.info("Updating {class_name} with id: {{}}", id);
        {class_name}DTO updated = service.update(id, dto);
        return ResponseEntity.ok(updated);
    }}

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {{
        log.info("Deleting {class_name} with id: {{}}", id);
        service.delete(id);
        return ResponseEntity.noContent().build();
    }}
}}'''
    
    def _generate_java_service(self, class_name: str) -> str:
        """Generate Java Service code"""
        return f'''package com.example.service;

import com.example.dto.{class_name}DTO;
import com.example.entity.{class_name}Entity;
import com.example.repository.{class_name}Repository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import javax.persistence.EntityNotFoundException;
import java.util.List;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class {class_name}Service {{

    private final {class_name}Repository repository;

    @Transactional
    public {class_name}DTO create({class_name}DTO dto) {{
        log.debug("Creating {class_name}: {{}}", dto);
        
        // Convert DTO to Entity
        {class_name}Entity entity = convertToEntity(dto);
        
        // Apply business logic here
        validateBusinessRules(entity);
        
        // Save to database
        {class_name}Entity saved = repository.save(entity);
        
        log.info("Successfully created {class_name} with id: {{}}", saved.getId());
        return convertToDTO(saved);
    }}

    @Transactional(readOnly = true)
    public {class_name}DTO findById(Long id) {{
        log.debug("Finding {class_name} with id: {{}}", id);
        {class_name}Entity entity = repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Entity not found with id: " + id));
        return convertToDTO(entity);
    }}

    @Transactional(readOnly = true)
    public List<{class_name}DTO> findAll() {{
        log.debug("Finding all {class_name}s");
        return repository.findAll().stream()
            .map(this::convertToDTO)
            .collect(Collectors.toList());
    }}

    @Transactional
    public {class_name}DTO update(Long id, {class_name}DTO dto) {{
        log.debug("Updating {class_name} with id: {{}}", id);
        
        {class_name}Entity existing = repository.findById(id)
            .orElseThrow(() -> new EntityNotFoundException("Entity not found with id: " + id));
        
        // Update fields
        updateEntityFromDTO(existing, dto);
        validateBusinessRules(existing);
        
        {class_name}Entity updated = repository.save(existing);
        log.info("Successfully updated {class_name} with id: {{}}", id);
        
        return convertToDTO(updated);
    }}

    @Transactional
    public void delete(Long id) {{
        log.debug("Deleting {class_name} with id: {{}}", id);
        if (!repository.existsById(id)) {{
            throw new EntityNotFoundException("Entity not found with id: " + id);
        }}
        repository.deleteById(id);
        log.info("Successfully deleted {class_name} with id: {{}}", id);
    }}

    private void validateBusinessRules({class_name}Entity entity) {{
        // Add business validation logic here
        log.debug("Validating business rules for {class_name}");
    }}

    private {class_name}Entity convertToEntity({class_name}DTO dto) {{
        // Use MapStruct or manual mapping
        {class_name}Entity entity = new {class_name}Entity();
        // Map fields
        return entity;
    }}

    private {class_name}DTO convertToDTO({class_name}Entity entity) {{
        // Use MapStruct or manual mapping
        {class_name}DTO dto = new {class_name}DTO();
        // Map fields
        return dto;
    }}

    private void updateEntityFromDTO({class_name}Entity entity, {class_name}DTO dto) {{
        // Update entity fields from DTO
    }}
}}'''
    
    def _generate_java_repository(self, class_name: str) -> str:
        """Generate Java Repository code"""
        return f'''package com.example.repository;

import com.example.entity.{class_name}Entity;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface {class_name}Repository extends JpaRepository<{class_name}Entity, Long> {{

    // Add custom query methods here
    // Example: Optional<{class_name}Entity> findByName(String name);
    
    // Example custom query
    // @Query("SELECT e FROM {class_name}Entity e WHERE e.status = :status")
    // List<{class_name}Entity> findByStatus(String status);
}}'''
    
    def _generate_java_dto(self, class_name: str) -> str:
        """Generate Java DTO code"""
        return f'''package com.example.dto;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Size;
import java.time.LocalDateTime;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {class_name}DTO {{

    private Long id;

    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    private String name;

    @NotBlank(message = "Description is required")
    @Size(max = 500, message = "Description cannot exceed 500 characters")
    private String description;

    @NotNull(message = "Status is required")
    private String status;

    private LocalDateTime createdAt;
    
    private LocalDateTime updatedAt;

    // Add additional fields based on requirements
}}'''
    
    def _generate_java_entity(self, class_name: str) -> str:
        """Generate Java Entity code"""
        return f'''package com.example.entity;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import javax.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "{class_name.lower()}s")
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class {class_name}Entity {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, length = 100)
    private String name;

    @Column(length = 500)
    private String description;

    @Column(nullable = false)
    private String status;

    @CreationTimestamp
    @Column(nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(nullable = false)
    private LocalDateTime updatedAt;

    // Add additional fields, relationships, and indexes based on requirements
}}'''
    
    def _generate_angular_component(self, class_name: str) -> str:
        """Generate Angular Component TypeScript code"""
        component_name = self._to_kebab_case(class_name)
        return f'''import {{ Component, OnInit, OnDestroy }} from '@angular/core';
import {{ FormBuilder, FormGroup, Validators }} from '@angular/forms';
import {{ Subject }} from 'rxjs';
import {{ takeUntil }} from 'rxjs/operators';
import {{ {class_name}Service }} from './{component_name}.service';
import {{ {class_name}Model }} from './{component_name}.model';

@Component({{
  selector: 'app-{component_name}',
  templateUrl: './{component_name}.component.html',
  styleUrls: ['./{component_name}.component.scss']
}})
export class {class_name}Component implements OnInit, OnDestroy {{
  
  {component_name}Form: FormGroup;
  items: {class_name}Model[] = [];
  loading = false;
  errorMessage: string | null = null;
  successMessage: string | null = null;
  
  private destroy$ = new Subject<void>();

  constructor(
    private fb: FormBuilder,
    private {component_name}Service: {class_name}Service
  ) {{
    this.{component_name}Form = this.createForm();
  }}

  ngOnInit(): void {{
    this.loadItems();
  }}

  ngOnDestroy(): void {{
    this.destroy$.next();
    this.destroy$.complete();
  }}

  private createForm(): FormGroup {{
    return this.fb.group({{
      name: ['', [Validators.required, Validators.minLength(2), Validators.maxLength(100)]],
      description: ['', [Validators.required, Validators.maxLength(500)]],
      status: ['', Validators.required]
    }});
  }}

  loadItems(): void {{
    this.loading = true;
    this.errorMessage = null;
    
    this.{component_name}Service.getAll()
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: (items) => {{
          this.items = items;
          this.loading = false;
        }},
        error: (error) => {{
          this.errorMessage = 'Failed to load items. Please try again.';
          this.loading = false;
          console.error('Error loading items:', error);
        }}
      }});
  }}

  onSubmit(): void {{
    if (this.{component_name}Form.invalid) {{
      this.{component_name}Form.markAllAsTouched();
      return;
    }}

    this.loading = true;
    this.errorMessage = null;
    this.successMessage = null;

    const formValue = this.{component_name}Form.value;

    this.{component_name}Service.create(formValue)
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: (created) => {{
          this.successMessage = 'Item created successfully!';
          this.{component_name}Form.reset();
          this.loadItems();
          this.loading = false;
        }},
        error: (error) => {{
          this.errorMessage = 'Failed to create item. Please try again.';
          this.loading = false;
          console.error('Error creating item:', error);
        }}
      }});
  }}

  onDelete(id: number): void {{
    if (!confirm('Are you sure you want to delete this item?')) {{
      return;
    }}

    this.loading = true;
    
    this.{component_name}Service.delete(id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({{
        next: () => {{
          this.successMessage = 'Item deleted successfully!';
          this.loadItems();
          this.loading = false;
        }},
        error: (error) => {{
          this.errorMessage = 'Failed to delete item. Please try again.';
          this.loading = false;
          console.error('Error deleting item:', error);
        }}
      }});
  }}

  isFieldInvalid(fieldName: string): boolean {{
    const field = this.{component_name}Form.get(fieldName);
    return !!(field && field.invalid && (field.dirty || field.touched));
  }}

  getFieldError(fieldName: string): string {{
    const field = this.{component_name}Form.get(fieldName);
    if (field?.errors) {{
      if (field.errors['required']) return 'This field is required';
      if (field.errors['minlength']) return `Minimum length is ${{field.errors['minlength'].requiredLength}}`;
      if (field.errors['maxlength']) return `Maximum length is ${{field.errors['maxlength'].requiredLength}}`;
    }}
    return '';
  }}
}}'''
    
    def _generate_angular_template(self, class_name: str) -> str:
        """Generate Angular Template HTML code"""
        component_name = self._to_kebab_case(class_name)
        return f'''<div class="{component_name}-container">
  <h2>{class_name} Management</h2>

  <!-- Success/Error Messages -->
  <div *ngIf="successMessage" class="alert alert-success">
    {{{{ successMessage }}}}
  </div>
  <div *ngIf="errorMessage" class="alert alert-error">
    {{{{ errorMessage }}}}
  </div>

  <!-- Form -->
  <div class="form-container">
    <h3>Create New {class_name}</h3>
    <form [formGroup]="{component_name}Form" (ngSubmit)="onSubmit()">
      
      <div class="form-group">
        <label for="name">Name *</label>
        <input 
          id="name" 
          type="text" 
          formControlName="name"
          [class.invalid]="isFieldInvalid('name')"
          placeholder="Enter name">
        <span class="error-message" *ngIf="isFieldInvalid('name')">
          {{{{ getFieldError('name') }}}}
        </span>
      </div>

      <div class="form-group">
        <label for="description">Description *</label>
        <textarea 
          id="description" 
          formControlName="description"
          [class.invalid]="isFieldInvalid('description')"
          placeholder="Enter description"
          rows="4"></textarea>
        <span class="error-message" *ngIf="isFieldInvalid('description')">
          {{{{ getFieldError('description') }}}}
        </span>
      </div>

      <div class="form-group">
        <label for="status">Status *</label>
        <select 
          id="status" 
          formControlName="status"
          [class.invalid]="isFieldInvalid('status')">
          <option value="">Select status</option>
          <option value="active">Active</option>
          <option value="inactive">Inactive</option>
          <option value="pending">Pending</option>
        </select>
        <span class="error-message" *ngIf="isFieldInvalid('status')">
          {{{{ getFieldError('status') }}}}
        </span>
      </div>

      <div class="form-actions">
        <button 
          type="submit" 
          [disabled]="loading || {component_name}Form.invalid"
          class="btn btn-primary">
          {{{{ loading ? 'Saving...' : 'Create' }}}}
        </button>
        <button 
          type="button" 
          (click)="{component_name}Form.reset()"
          [disabled]="loading"
          class="btn btn-secondary">
          Reset
        </button>
      </div>
    </form>
  </div>

  <!-- Items List -->
  <div class="items-container">
    <h3>Existing {class_name}s</h3>
    
    <div *ngIf="loading" class="loading-spinner">
      Loading...
    </div>

    <table *ngIf="!loading && items.length > 0" class="items-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Description</th>
          <th>Status</th>
          <th>Created At</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr *ngFor="let item of items">
          <td>{{{{ item.id }}}}</td>
          <td>{{{{ item.name }}}}</td>
          <td>{{{{ item.description }}}}</td>
          <td>
            <span [class]="'status-badge status-' + item.status">
              {{{{ item.status }}}}
            </span>
          </td>
          <td>{{{{ item.createdAt | date:'short' }}}}</td>
          <td>
            <button 
              (click)="onDelete(item.id)" 
              [disabled]="loading"
              class="btn btn-danger btn-sm">
              Delete
            </button>
          </td>
        </tr>
      </tbody>
    </table>

    <div *ngIf="!loading && items.length === 0" class="no-items">
      No items found. Create one using the form above.
    </div>
  </div>
</div>'''
    
    def _generate_angular_styles(self) -> str:
        """Generate Angular Component SCSS code"""
        return '''.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2, h3 {
  color: #333;
  margin-bottom: 20px;
}

/* Alerts */
.alert {
  padding: 12px 20px;
  margin-bottom: 20px;
  border-radius: 4px;
  
  &.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
  }
  
  &.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
  }
}

/* Form */
.form-container {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.form-group {
  margin-bottom: 20px;
  
  label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: #555;
  }
  
  input, textarea, select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 14px;
    
    &:focus {
      outline: none;
      border-color: #4CAF50;
      box-shadow: 0 0 0 2px rgba(76, 175, 80, 0.2);
    }
    
    &.invalid {
      border-color: #dc3545;
    }
  }
  
  .error-message {
    display: block;
    color: #dc3545;
    font-size: 12px;
    margin-top: 4px;
  }
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 24px;
}

/* Buttons */
.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.3s;
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
  
  &.btn-primary {
    background-color: #4CAF50;
    color: white;
    
    &:hover:not(:disabled) {
      background-color: #45a049;
    }
  }
  
  &.btn-secondary {
    background-color: #6c757d;
    color: white;
    
    &:hover:not(:disabled) {
      background-color: #5a6268;
    }
  }
  
  &.btn-danger {
    background-color: #dc3545;
    color: white;
    
    &:hover:not(:disabled) {
      background-color: #c82333;
    }
  }
  
  &.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
  }
}

/* Items Container */
.items-container {
  background: white;
  padding: 24px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.items-table {
  width: 100%;
  border-collapse: collapse;
  
  thead {
    background-color: #f8f9fa;
    
    th {
      padding: 12px;
      text-align: left;
      font-weight: 600;
      color: #333;
      border-bottom: 2px solid #dee2e6;
    }
  }
  
  tbody {
    tr {
      border-bottom: 1px solid #dee2e6;
      
      &:hover {
        background-color: #f8f9fa;
      }
      
      td {
        padding: 12px;
      }
    }
  }
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
  
  &.status-active {
    background-color: #d4edda;
    color: #155724;
  }
  
  &.status-inactive {
    background-color: #f8d7da;
    color: #721c24;
  }
  
  &.status-pending {
    background-color: #fff3cd;
    color: #856404;
  }
}

.loading-spinner {
  text-align: center;
  padding: 40px;
  color: #666;
}

.no-items {
  text-align: center;
  padding: 40px;
  color: #999;
}'''
    
    def _generate_angular_service(self, class_name: str) -> str:
        """Generate Angular Service code"""
        component_name = self._to_kebab_case(class_name)
        return f'''import {{ Injectable }} from '@angular/core';
import {{ HttpClient, HttpHeaders }} from '@angular/common/http';
import {{ Observable, throwError }} from 'rxjs';
import {{ catchError, map }} from 'rxjs/operators';
import {{ {class_name}Model }} from './{component_name}.model';

@Injectable({{
  providedIn: 'root'
}})
export class {class_name}Service {{

  private apiUrl = '/api/{component_name}'; // Update with your API base URL

  private httpOptions = {{
    headers: new HttpHeaders({{
      'Content-Type': 'application/json'
    }})
  }};

  constructor(private http: HttpClient) {{ }}

  /**
   * Get all items
   */
  getAll(): Observable<{class_name}Model[]> {{
    return this.http.get<{class_name}Model[]>(this.apiUrl)
      .pipe(
        catchError(this.handleError)
      );
  }}

  /**
   * Get item by ID
   */
  getById(id: number): Observable<{class_name}Model> {{
    const url = `${{this.apiUrl}}/${{id}}`;
    return this.http.get<{class_name}Model>(url)
      .pipe(
        catchError(this.handleError)
      );
  }}

  /**
   * Create new item
   */
  create(item: Partial<{class_name}Model>): Observable<{class_name}Model> {{
    return this.http.post<{class_name}Model>(this.apiUrl, item, this.httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }}

  /**
   * Update existing item
   */
  update(id: number, item: Partial<{class_name}Model>): Observable<{class_name}Model> {{
    const url = `${{this.apiUrl}}/${{id}}`;
    return this.http.put<{class_name}Model>(url, item, this.httpOptions)
      .pipe(
        catchError(this.handleError)
      );
  }}

  /**
   * Delete item
   */
  delete(id: number): Observable<void> {{
    const url = `${{this.apiUrl}}/${{id}}`;
    return this.http.delete<void>(url)
      .pipe(
        catchError(this.handleError)
      );
  }}

  /**
   * Handle HTTP errors
   */
  private handleError(error: any): Observable<never> {{
    let errorMessage = 'An error occurred';
    
    if (error.error instanceof ErrorEvent) {{
      // Client-side error
      errorMessage = `Error: ${{error.error.message}}`;
    }} else {{
      // Server-side error
      errorMessage = `Error Code: ${{error.status}}\\nMessage: ${{error.message}}`;
    }}
    
    console.error(errorMessage);
    return throwError(() => new Error(errorMessage));
  }}
}}'''
    
    def _generate_angular_model(self, class_name: str) -> str:
        """Generate Angular Model/Interface code"""
        return f'''export interface {class_name}Model {{
  id: number;
  name: string;
  description: string;
  status: string;
  createdAt: Date;
  updatedAt: Date;
}}

export interface Create{class_name}Request {{
  name: string;
  description: string;
  status: string;
}}

export interface Update{class_name}Request {{
  name?: string;
  description?: string;
  status?: string;
}}'''
'''
'''
