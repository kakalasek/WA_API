from flask import Blueprint, jsonify

about_bp = Blueprint("about", __name__)

@about_bp.get("/")
def about():
    docs = {
        "endpoints":{ 
            "/api/auth": {
                "/register": {
                    "description": "Registers the user",
                    "method": "POST",
                    "json-format": "{ username: <username>, password: <password> }",
                    "return-format": "{ message: User created }",
                    "status-code": 201,
                    "errors": {
                        "user-already-exists": {
                            "description": "The user already exists",
                            "return-format": "{ error: User already exists}",
                            "status-code": 403
                        }
                    }
                },
                "/login": {
                    "description": "Logs in a user",
                    "method": "POST",
                    "json-format": "{ username: <username>, password: <password> }",
                    "return-format": "{ message: Logged In, tokens: { access: <access_token>, refresh: <refresh_token> } }",
                    "status-code": 200,
                    "errors": {
                        "invalid-credentials": {
                            "description": "Provided credentials either dont belong to any registered user, or the password is wrong",
                            "return-format": "{ error: Invalid username or password }",
                            "status-code": 400
                        }
                    }
                },
                "/whoami": {
                    "description": "Returns the username of a logged user based on his access token",
                    "method": "GET",
                    "authorization": "Required",
                    "headers": "{ Authorization: Bearer <access_token> }",
                    "return-format": "{ message: message, user_details: { username: <username> }}",
                    "status-code": 200
                },
                "/refresh": {
                    "description": "Return new access token after its expiration using the refresh token",
                    "method": "GET",
                    "authorization": "Required",
                    "headers": "{ Authorization: Bearer <refresh_token> }",
                    "return-format": "{ access_token: <new_access_token> }",
                    "status-code": 200
                },
                "/logout": {
                    "description": "Revokes either an access or refresh token, based on what is provided",
                    "method": "GET",
                    "authorization": "Required",
                    "headers": "{ Authorization: Bearer <refresh_token|access_token> }",
                    "return-format": "{ message: <token_type> token revoked successfully}",
                    "status-code": 200
                }
            },
            "/api/users": {
                "/all": {
                    "description": "Returns all registered users",
                    "method": "GET",
                    "authorization": "Required",
                    "admin-only": True,
                    "headers": "{ Authorization: Bearer <access_token> }",
                    "return-format": "{ users: [ { username: <username> }, ... ]}",
                    "status-code": 200,
                    "errors": {
                        "not-admin": {
                            "description": "You do not have admin priviliges, thus you cant view all the users",
                            "return-format": "{ message: You are not authorized to access this}",
                            "status-code": 401
                        }
                    }
                }
            },
            "/api/blog": {
                "/": {
                    "method": {
                        "GET": {
                            "description": "Returns all existing posts",
                            "return-format": "{ {user: <username>, date: <datetime_of_creation>, text: <content_of_post>}...}",
                            "status-code": 200
                        },
                        "POST": {
                            "description": "Creates a new blog post",
                            "authorization": "Required",
                            "headers": "{ Authorization: Bearer <access_token> }",
                            "json-format": "{ text: <content_of_post> }",
                            "return-format": "{ message: Post created successfully}",
                            "status-code": 201
                        }
                    }
                },
                "/<post_id>": {
                    "method": {
                        "GET": {
                            "description": "Returns a post with the specified ID",
                            "return-format": "{ user: <username>, date: <datetime_of_creation>, text: <content_of_post> }",
                            "status-code": 200,
                            "errors": {
                                "post-not-found": {
                                    "description": "Post with the specified ID does not exist",
                                    "return-format": "{ error: Post with this ID does not exist }",
                                    "status-code": 404
                                }
                            }
                        },
                        "PATCH": {
                            "description": "Updates content of the post with the specified ID",
                            "authorization": "Required",
                            "headers": "{ Authorization: Bearer <access_token> }",
                            "return-format": "{ message: Post patched successfully }",
                            "status-code": 200,
                            "errors": {
                                "post-not-found": {
                                    "description": "Post with the specified ID does not exist",
                                    "return-format": "{ error: Post with this ID does not exist }",
                                    "status-code": 404
                                },
                                "unathorized-patch": {
                                    "description": "You are not authorized to modify this post",
                                    "return-format": "{ message: You are not authorized to patch the post with this ID, error: unauthorized_patch }",
                                    "status-code": 401
                                }
                            }
                        },
                        "DELETE": {
                            "description": "Deletes the post with the specified ID",
                            "authorization": "Required",
                            "headers": "{ Authorization: Bearer <access_token> }",
                            "return-format": "{ message: Post deleted successfully }",
                            "status-code": 200,
                            "errors": {
                                "post-not-found": {
                                    "description": "Post with the specified ID does not exist",
                                    "return-format": "{ error: Post with this ID does not exist }",
                                    "status-code": 404
                                },
                                "unathorized-delete": {
                                    "description": "You are not authorized to delete this post",
                                    "return-format": "{ message: You are not authorized to delete the post with this ID, error: unauthorized_delete }",
                                    "status-code": 401
                                }
                            }
                        }
                    }
                }
            } 
        },
        "authorization": {
            "explanation": "Authentication and authorization are JWT based. You log in and get a jwt access and jwt refresh token. You provide your access token with every request that requires authorization and the refresh token, if you want to restore an expired token. Logout simply revokes either an access token or a refresh token, based on whats provided.",
            "description": "If the endpoint says authorization: Required, the endpoint may throw the following errors",
            "errors": {
                "token-expired": {
                    "description": "Your token has expired",
                    "return-format": "{ message: Token has expired, error: token_expired }",
                    "status-code": 401
                },
                "invalid-token": {
                    "description": "Your token is invalid",
                    "return-format": "{ message: Signature verification failed, error: invalid_token }",
                    "status-code": 401
                },
                "missing-token": {
                    "description": "Your token is missing from the request",
                    "return-format": "{ message: Request does not contain a valid token, error: authorization_required}",
                    "status-code": 401
                },
            }
        }
                        
    }

    return jsonify(docs), 200