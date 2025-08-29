# ---- Builder Stage ----
# Use a full Go image to build our application
FROM golang:alpine3.22 as builder

WORKDIR /app

# Copy the Go module files and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go application. CGO_ENABLED=0 is important for a static binary.
RUN CGO_ENABLED=0 GOOS=linux go build -v -o /app/server ./...

# ---- Final Stage ----
# Use a minimal, non-root image for the final product
FROM gcr.io/distroless/static-debian11

WORKDIR /

# Copy the built binary from the builder stage
COPY --from=builder /app/server /server

# Expose the port the app runs on
EXPOSE 8080

# The command to run our application
CMD ["/server"]