---
layout: default
title: "Kubernetes Operator Patterns - Chapter 6: Testing Operators"
nav_order: 6
has_children: false
parent: Kubernetes Operator Patterns
---

# Chapter 6: Testing Operators - Unit Tests, Integration Tests, and envtest Framework

> Master comprehensive testing strategies for Kubernetes operators including unit tests, integration tests, and envtest framework.

## Overview

Testing operators is critical for reliability and maintainability. This chapter covers unit testing, integration testing, and using the envtest framework to test operators against a real Kubernetes API server.

## Unit Testing

### Controller Unit Tests

```go
// Controller unit tests
package controllers

import (
    "context"
    "testing"
    "time"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client/fake"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

func TestDatabaseReconciler(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Database Controller Suite")
}

var _ = Describe("Database Controller", func() {
    var (
        reconciler *DatabaseReconciler
        req        ctrl.Request
        ctx        context.Context
        database   *postgresqlv1.Database
    )

    BeforeEach(func() {
        // Setup
        ctx = context.Background()

        // Create a fake client with the scheme
        scheme := runtime.NewScheme()
        postgresqlv1.AddToScheme(scheme)
        appsv1.AddToScheme(scheme)
        corev1.AddToScheme(scheme)

        fakeClient := fake.NewClientBuilder().WithScheme(scheme).Build()

        // Create reconciler
        reconciler = &DatabaseReconciler{
            Client:   fakeClient,
            Scheme:   scheme,
            Recorder: nil, // Can be mocked if needed
        }

        // Create test database
        database = &postgresqlv1.Database{
            ObjectMeta: metav1.ObjectMeta{
                Name:      "test-db",
                Namespace: "default",
                UID:       "test-uid",
            },
            Spec: postgresqlv1.DatabaseSpec{
                Engine:  "postgresql",
                Version: "14",
                Replicas: 1,
            },
        }

        req = ctrl.Request{
            NamespacedName: types.NamespacedName{
                Name:      database.Name,
                Namespace: database.Namespace,
            },
        }
    })

    Context("When reconciling a Database", func() {
        It("should create the required resources", func() {
            // Create the database resource
            err := reconciler.Client.Create(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Run reconciliation
            result, err := reconciler.Reconcile(ctx, req)
            Expect(err).NotTo(HaveOccurred())
            Expect(result.Requeue).To(BeFalse())

            // Check that deployment was created
            deployment := &appsv1.Deployment{}
            err = reconciler.Client.Get(ctx, types.NamespacedName{
                Name:      "test-db-deployment",
                Namespace: "default",
            }, deployment)
            Expect(err).NotTo(HaveOccurred())
            Expect(*deployment.Spec.Replicas).To(Equal(int32(1)))

            // Check that service was created
            service := &corev1.Service{}
            err = reconciler.Client.Get(ctx, types.NamespacedName{
                Name:      "test-db-service",
                Namespace: "default",
            }, service)
            Expect(err).NotTo(HaveOccurred())
            Expect(service.Spec.Type).To(Equal(corev1.ServiceTypeClusterIP))
        })

        It("should update deployment when spec changes", func() {
            // Create initial database
            database.Spec.Replicas = 1
            err := reconciler.Client.Create(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Run initial reconciliation
            _, err = reconciler.Reconcile(ctx, req)
            Expect(err).NotTo(HaveOccurred())

            // Update spec
            err = reconciler.Client.Get(ctx, req.NamespacedName, database)
            Expect(err).NotTo(HaveOccurred())
            database.Spec.Replicas = 3
            err = reconciler.Client.Update(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Run reconciliation again
            _, err = reconciler.Reconcile(ctx, req)
            Expect(err).NotTo(HaveOccurred())

            // Check deployment was updated
            deployment := &appsv1.Deployment{}
            err = reconciler.Client.Get(ctx, types.NamespacedName{
                Name:      "test-db-deployment",
                Namespace: "default",
            }, deployment)
            Expect(err).NotTo(HaveOccurred())
            Expect(*deployment.Spec.Replicas).To(Equal(int32(3)))
        })

        It("should handle not found errors gracefully", func() {
            // Try to reconcile non-existent resource
            nonExistentReq := ctrl.Request{
                NamespacedName: types.NamespacedName{
                    Name:      "non-existent",
                    Namespace: "default",
                },
            }

            result, err := reconciler.Reconcile(ctx, nonExistentReq)
            Expect(err).NotTo(HaveOccurred())
            Expect(result.Requeue).To(BeFalse())
        })
    })
})
```

### Helper Function Testing

```go
// Helper function unit tests
package controllers

import (
    "testing"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

func TestBuildDeployment(t *testing.T) {
    reconciler := &DatabaseReconciler{}

    database := &postgresqlv1.Database{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "test-db",
            Namespace: "test-ns",
        },
        Spec: postgresqlv1.DatabaseSpec{
            Engine:   "postgresql",
            Version:  "14",
            Replicas: 2,
            Image:    "postgres:14",
        },
    }

    deployment := reconciler.buildDeployment(database)

    // Test basic properties
    if deployment.Name != "test-db-deployment" {
        t.Errorf("Expected deployment name 'test-db-deployment', got %s", deployment.Name)
    }

    if deployment.Namespace != "test-ns" {
        t.Errorf("Expected namespace 'test-ns', got %s", deployment.Namespace)
    }

    // Test spec
    if *deployment.Spec.Replicas != 2 {
        t.Errorf("Expected 2 replicas, got %d", *deployment.Spec.Replicas)
    }

    // Test container
    container := deployment.Spec.Template.Spec.Containers[0]
    if container.Image != "postgres:14" {
        t.Errorf("Expected image 'postgres:14', got %s", container.Image)
    }

    // Test labels
    expectedLabels := map[string]string{
        "app.kubernetes.io/name":       "test-db",
        "app.kubernetes.io/instance":   "test-db",
        "app.kubernetes.io/version":    "",
        "app.kubernetes.io/component":  "database",
        "app.kubernetes.io/part-of":    "postgresql-operator",
        "app.kubernetes.io/managed-by": "postgresql-operator",
    }

    for key, expectedValue := range expectedLabels {
        if actualValue, exists := deployment.Labels[key]; !exists || actualValue != expectedValue {
            t.Errorf("Expected label %s=%s, got %s", key, expectedValue, actualValue)
        }
    }
}

func TestBuildService(t *testing.T) {
    reconciler := &DatabaseReconciler{}

    database := &postgresqlv1.Database{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "test-db",
            Namespace: "test-ns",
        },
        Spec: postgresqlv1.DatabaseSpec{
            Engine:  "postgresql",
            Version: "14",
        },
    }

    service := reconciler.buildService(database)

    // Test basic properties
    if service.Name != "test-db-service" {
        t.Errorf("Expected service name 'test-db-service', got %s", service.Name)
    }

    // Test ports
    if len(service.Spec.Ports) != 1 {
        t.Errorf("Expected 1 port, got %d", len(service.Spec.Ports))
    }

    port := service.Spec.Ports[0]
    if port.Port != 5432 {
        t.Errorf("Expected port 5432, got %d", port.Port)
    }

    if port.TargetPort.StrVal != "postgresql" {
        t.Errorf("Expected target port 'postgresql', got %s", port.TargetPort.StrVal)
    }
}

func TestGetResourceName(t *testing.T) {
    reconciler := &DatabaseReconciler{}

    database := &postgresqlv1.Database{
        ObjectMeta: metav1.ObjectMeta{
            Name: "my-database",
        },
    }

    testCases := []struct {
        suffix   string
        expected string
    }{
        {"deployment", "my-database-deployment"},
        {"service", "my-database-service"},
        {"config", "my-database-config"},
        {"pvc", "my-database-pvc"},
    }

    for _, tc := range testCases {
        result := reconciler.getResourceName(database, tc.suffix)
        if result != tc.expected {
            t.Errorf("getResourceName(%s) = %s, expected %s", tc.suffix, result, tc.expected)
        }
    }
}
```

### Mock Testing

```go
// Mock client for testing
package controllers

import (
    "context"
    "testing"

    "github.com/golang/mock/gomock"
    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/runtime"
    "k8s.io/apimachinery/pkg/types"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/reconcile"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

type mockClient struct {
    objects map[types.NamespacedName]runtime.Object
}

func (m *mockClient) Get(ctx context.Context, key client.ObjectKey, obj client.Object) error {
    nsName := types.NamespacedName{Name: key.Name, Namespace: key.Namespace}
    if stored, exists := m.objects[nsName]; exists {
        // Copy stored object to obj
        stored.DeepCopyInto(obj.(runtime.Object))
        return nil
    }
    return fmt.Errorf("object not found")
}

func (m *mockClient) Create(ctx context.Context, obj client.Object, opts ...client.CreateOption) error {
    nsName := types.NamespacedName{
        Name:      obj.GetName(),
        Namespace: obj.GetNamespace(),
    }
    m.objects[nsName] = obj.DeepCopyObject()
    return nil
}

func TestReconcilerWithMock(t *testing.T) {
    // Create mock client
    mockClient := &mockClient{
        objects: make(map[types.NamespacedName]runtime.Object),
    }

    // Create reconciler with mock client
    reconciler := &DatabaseReconciler{
        Client: mockClient,
        Scheme: runtime.NewScheme(),
    }

    // Create test database
    database := &postgresqlv1.Database{
        ObjectMeta: metav1.ObjectMeta{
            Name:      "test-db",
            Namespace: "default",
        },
        Spec: postgresqlv1.DatabaseSpec{
            Engine:   "postgresql",
            Version:  "14",
            Replicas: 1,
        },
    }

    req := reconcile.Request{
        NamespacedName: types.NamespacedName{
            Name:      database.Name,
            Namespace: database.Namespace,
        },
    }

    // Run reconciliation
    result, err := reconciler.Reconcile(context.Background(), req)

    // Assertions
    if err != nil {
        t.Fatalf("Reconciliation failed: %v", err)
    }

    if result.Requeue {
        t.Error("Expected no requeue, but got requeue")
    }

    // Check that deployment was created in mock
    deployment := &appsv1.Deployment{}
    err = mockClient.Get(context.Background(),
        client.ObjectKey{Name: "test-db-deployment", Namespace: "default"},
        deployment)

    if err != nil {
        t.Fatalf("Deployment was not created: %v", err)
    }

    if *deployment.Spec.Replicas != 1 {
        t.Errorf("Expected 1 replica, got %d", *deployment.Spec.Replicas)
    }
}
```

## Integration Testing

### envtest Framework

```go
// Integration tests with envtest
package controllers

import (
    "context"
    "path/filepath"
    "testing"
    "time"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/types"
    "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/envtest"
    "sigs.k8s.io/controller-runtime/pkg/manager"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

var (
    testEnv   *envtest.Environment
    k8sClient client.Client
    ctx       context.Context
    cancel    context.CancelFunc
)

func TestControllers(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Controller Suite")
}

var _ = BeforeSuite(func() {
    ctx, cancel = context.WithCancel(context.Background())

    // Setup test environment
    testEnv = &envtest.Environment{
        CRDDirectoryPaths:     []string{filepath.Join("..", "config", "crd", "bases")},
        ErrorIfCRDPathMissing: true,
    }

    cfg, err := testEnv.Start()
    Expect(err).NotTo(HaveOccurred())
    Expect(cfg).NotTo(BeNil())

    // Add schemes
    err = postgresqlv1.AddToScheme(scheme.Scheme)
    Expect(err).NotTo(HaveOccurred())

    // Create client
    k8sClient, err = client.New(cfg, client.Options{Scheme: scheme.Scheme})
    Expect(err).NotTo(HaveOccurred())
    Expect(k8sClient).NotTo(BeNil())
})

var _ = AfterSuite(func() {
    cancel()
    err := testEnv.Stop()
    Expect(err).NotTo(HaveOccurred())
})

var _ = Describe("Database Controller Integration", func() {
    var reconciler *DatabaseReconciler
    var mgr manager.Manager

    BeforeEach(func() {
        // Setup manager
        var err error
        mgr, err = ctrl.NewManager(testEnv.Config, ctrl.Options{
            Scheme: scheme.Scheme,
        })
        Expect(err).NotTo(HaveOccurred())

        // Create reconciler
        reconciler = &DatabaseReconciler{
            Client:   mgr.GetClient(),
            Scheme:   mgr.GetScheme(),
            Recorder: mgr.GetEventRecorderFor("database-controller"),
        }

        // Register reconciler
        err = reconciler.SetupWithManager(mgr)
        Expect(err).NotTo(HaveOccurred())

        // Start manager in goroutine
        go func() {
            defer GinkgoRecover()
            err := mgr.Start(ctx)
            Expect(err).NotTo(HaveOccurred())
        }()
    })

    Context("When creating a Database", func() {
        It("should create associated resources", func() {
            database := &postgresqlv1.Database{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "test-db",
                    Namespace: "default",
                },
                Spec: postgresqlv1.DatabaseSpec{
                    Engine:   "postgresql",
                    Version:  "14",
                    Replicas: 1,
                    Image:    "postgres:14",
                },
            }

            // Create database
            err := k8sClient.Create(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Wait for reconciliation
            time.Sleep(2 * time.Second)

            // Check deployment was created
            deployment := &appsv1.Deployment{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-db-deployment",
                    Namespace: "default",
                }, deployment)
            }, 10*time.Second, 1*time.Second).Should(Succeed())

            Expect(*deployment.Spec.Replicas).To(Equal(int32(1)))
            Expect(deployment.Spec.Template.Spec.Containers[0].Image).To(Equal("postgres:14"))

            // Check service was created
            service := &corev1.Service{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-db-service",
                    Namespace: "default",
                }, service)
            }, 10*time.Second, 1*time.Second).Should(Succeed())

            Expect(service.Spec.Type).To(Equal(corev1.ServiceTypeClusterIP))
        })

        It("should update resources when spec changes", func() {
            // Get existing database
            database := &postgresqlv1.Database{}
            err := k8sClient.Get(ctx, types.NamespacedName{
                Name:      "test-db",
                Namespace: "default",
            }, database)
            Expect(err).NotTo(HaveOccurred())

            // Update spec
            database.Spec.Replicas = 3
            err = k8sClient.Update(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Wait for update
            time.Sleep(2 * time.Second)

            // Check deployment was updated
            deployment := &appsv1.Deployment{}
            Eventually(func() int32 {
                err := k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-db-deployment",
                    Namespace: "default",
                }, deployment)
                if err != nil {
                    return 0
                }
                return *deployment.Spec.Replicas
            }, 10*time.Second, 1*time.Second).Should(Equal(int32(3)))
        })

        It("should handle resource deletion", func() {
            // Delete database
            database := &postgresqlv1.Database{}
            err := k8sClient.Get(ctx, types.NamespacedName{
                Name:      "test-db",
                Namespace: "default",
            }, database)
            Expect(err).NotTo(HaveOccurred())

            err = k8sClient.Delete(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Wait for deletion
            time.Sleep(2 * time.Second)

            // Check resources were deleted
            deployment := &appsv1.Deployment{}
            Eventually(func() bool {
                err := k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "test-db-deployment",
                    Namespace: "default",
                }, deployment)
                return errors.IsNotFound(err)
            }, 10*time.Second, 1*time.Second).Should(BeTrue())
        })
    })
})
```

### End-to-End Testing

```go
// E2E tests
package e2e

import (
    "context"
    "testing"
    "time"

    . "github.com/onsi/ginkgo/v2"
    . "github.com/onsi/gomega"

    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    "k8s.io/apimachinery/pkg/api/errors"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/apimachinery/pkg/types"
    "sigs.k8s.io/controller-runtime/pkg/client"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

func TestE2E(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "E2E Suite")
}

var _ = Describe("PostgreSQL Operator E2E", func() {
    var k8sClient client.Client
    ctx := context.Background()

    BeforeEach(func() {
        // Setup k8s client for real cluster
        // This would connect to a test cluster
    })

    Context("Database Lifecycle", func() {
        It("should create and manage a complete database", func() {
            database := &postgresqlv1.Database{
                ObjectMeta: metav1.ObjectMeta{
                    Name:      "e2e-test-db",
                    Namespace: "default",
                },
                Spec: postgresqlv1.DatabaseSpec{
                    Engine:   "postgresql",
                    Version:  "14",
                    Replicas: 1,
                    Image:    "postgres:14",
                },
            }

            // Create database
            err := k8sClient.Create(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Wait for deployment to be ready
            deployment := &appsv1.Deployment{}
            Eventually(func() bool {
                err := k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "e2e-test-db-deployment",
                    Namespace: "default",
                }, deployment)
                if err != nil {
                    return false
                }
                return deployment.Status.ReadyReplicas == *deployment.Spec.Replicas
            }, 5*time.Minute, 10*time.Second).Should(BeTrue())

            // Wait for service to be created
            service := &corev1.Service{}
            Eventually(func() error {
                return k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "e2e-test-db-service",
                    Namespace: "default",
                }, service)
            }, 1*time.Minute, 5*time.Second).Should(Succeed())

            // Check database status
            Eventually(func() string {
                err := k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "e2e-test-db",
                    Namespace: "default",
                }, database)
                if err != nil {
                    return ""
                }
                return string(database.Status.Phase)
            }, 5*time.Minute, 30*time.Second).Should(Equal("Running"))

            // Test scaling
            database.Spec.Replicas = 2
            err = k8sClient.Update(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Wait for scaling
            Eventually(func() int32 {
                err := k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "e2e-test-db-deployment",
                    Namespace: "default",
                }, deployment)
                if err != nil {
                    return 0
                }
                return deployment.Status.ReadyReplicas
            }, 3*time.Minute, 10*time.Second).Should(Equal(int32(2)))

            // Cleanup
            err = k8sClient.Delete(ctx, database)
            Expect(err).NotTo(HaveOccurred())

            // Wait for cleanup
            Eventually(func() bool {
                err := k8sClient.Get(ctx, types.NamespacedName{
                    Name:      "e2e-test-db",
                    Namespace: "default",
                }, database)
                return errors.IsNotFound(err)
            }, 2*time.Minute, 10*time.Second).Should(BeTrue())
        })
    })
})
```

## Test Utilities and Helpers

### Test Fixtures

```go
// Test fixtures and helpers
package testutils

import (
    appsv1 "k8s.io/api/apps/v1"
    corev1 "k8s.io/api/core/v1"
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "sigs.k8s.io/controller-runtime/pkg/client"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

// CreateTestDatabase creates a test database resource
func CreateTestDatabase(name, namespace string) *postgresqlv1.Database {
    return &postgresqlv1.Database{
        ObjectMeta: metav1.ObjectMeta{
            Name:      name,
            Namespace: namespace,
            Labels: map[string]string{
                "test": "true",
            },
        },
        Spec: postgresqlv1.DatabaseSpec{
            Engine:   "postgresql",
            Version:  "14",
            Replicas: 1,
            Image:    "postgres:14",
            Storage: &postgresqlv1.StorageSpec{
                Size:      "1Gi",
                ClassName: "standard",
            },
        },
    }
}

// CreateTestDeployment creates a test deployment
func CreateTestDeployment(name, namespace, image string, replicas int32) *appsv1.Deployment {
    return &appsv1.Deployment{
        ObjectMeta: metav1.ObjectMeta{
            Name:      name,
            Namespace: namespace,
        },
        Spec: appsv1.DeploymentSpec{
            Replicas: &replicas,
            Selector: &metav1.LabelSelector{
                MatchLabels: map[string]string{
                    "app": name,
                },
            },
            Template: corev1.PodTemplateSpec{
                ObjectMeta: metav1.ObjectMeta{
                    Labels: map[string]string{
                        "app": name,
                    },
                },
                Spec: corev1.PodSpec{
                    Containers: []corev1.Container{
                        {
                            Name:  "app",
                            Image: image,
                            Ports: []corev1.ContainerPort{
                                {
                                    ContainerPort: 5432,
                                    Name:          "postgresql",
                                },
                            },
                        },
                    },
                },
            },
        },
    }
}

// WaitForResource waits for a resource to reach a desired state
func WaitForResource(client client.Client, obj client.Object, checkFunc func() bool, timeout time.Duration) error {
    deadline := time.Now().Add(timeout)

    for time.Now().Before(deadline) {
        err := client.Get(context.Background(), client.ObjectKeyFromObject(obj), obj)
        if err != nil {
            return err
        }

        if checkFunc() {
            return nil
        }

        time.Sleep(1 * time.Second)
    }

    return fmt.Errorf("timeout waiting for resource condition")
}

// CheckDeploymentReady checks if deployment is ready
func CheckDeploymentReady(deployment *appsv1.Deployment) bool {
    return deployment.Status.ReadyReplicas == *deployment.Spec.Replicas &&
           deployment.Status.Replicas == *deployment.Spec.Replicas &&
           deployment.Status.AvailableReplicas == *deployment.Spec.Replicas
}
```

### Test Environment Setup

```go
// Test environment utilities
package testenv

import (
    "context"
    "testing"

    "k8s.io/client-go/kubernetes/scheme"
    ctrl "sigs.k8s.io/controller-runtime"
    "sigs.k8s.io/controller-runtime/pkg/client"
    "sigs.k8s.io/controller-runtime/pkg/envtest"
    "sigs.k8s.io/controller-runtime/pkg/manager"

    postgresqlv1 "github.com/example/postgresql-operator/api/v1"
)

type TestEnvironment struct {
    Env       *envtest.Environment
    Client    client.Client
    Manager   manager.Manager
    Ctx       context.Context
    Cancel    context.CancelFunc
}

func NewTestEnvironment() (*TestEnvironment, error) {
    ctx, cancel := context.WithCancel(context.Background())

    testEnv := &envtest.Environment{
        CRDDirectoryPaths:     []string{"config/crd/bases"},
        ErrorIfCRDPathMissing: true,
    }

    cfg, err := testEnv.Start()
    if err != nil {
        cancel()
        return nil, err
    }

    // Add schemes
    err = postgresqlv1.AddToScheme(scheme.Scheme)
    if err != nil {
        cancel()
        testEnv.Stop()
        return nil, err
    }

    // Create client
    k8sClient, err := client.New(cfg, client.Options{Scheme: scheme.Scheme})
    if err != nil {
        cancel()
        testEnv.Stop()
        return nil, err
    }

    // Create manager
    mgr, err := ctrl.NewManager(cfg, ctrl.Options{
        Scheme: scheme.Scheme,
    })
    if err != nil {
        cancel()
        testEnv.Stop()
        return nil, err
    }

    return &TestEnvironment{
        Env:     testEnv,
        Client:  k8sClient,
        Manager: mgr,
        Ctx:     ctx,
        Cancel:  cancel,
    }, nil
}

func (te *TestEnvironment) StartManager() error {
    go func() {
        if err := te.Manager.Start(te.Ctx); err != nil {
            panic(err)
        }
    }()
    return nil
}

func (te *TestEnvironment) Stop() error {
    te.Cancel()
    return te.Env.Stop()
}

func (te *TestEnvironment) CreateTestDatabase(name, namespace string) (*postgresqlv1.Database, error) {
    database := &postgresqlv1.Database{
        ObjectMeta: metav1.ObjectMeta{
            Name:      name,
            Namespace: namespace,
        },
        Spec: postgresqlv1.DatabaseSpec{
            Engine:   "postgresql",
            Version:  "14",
            Replicas: 1,
            Image:    "postgres:14",
        },
    }

    return database, te.Client.Create(te.Ctx, database)
}

// Usage in tests
func TestWithEnvironment(t *testing.T) {
    env, err := NewTestEnvironment()
    if err != nil {
        t.Fatal(err)
    }
    defer env.Stop()

    // Start manager
    err = env.StartManager()
    if err != nil {
        t.Fatal(err)
    }

    // Create test resources
    database, err := env.CreateTestDatabase("test-db", "default")
    if err != nil {
        t.Fatal(err)
    }

    // Run tests...
}
```

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        go-version: [1.19.x, 1.20.x]

    steps:
    - uses: actions/checkout@v3

    - name: Set up Go
      uses: actions/setup-go@v3
      with:
        go-version: ${{ matrix.go-version }}

    - name: Cache Go modules
      uses: actions/cache@v3
      with:
        path: ~/go/pkg/mod
        key: ${{ runner.os }}-go-${{ hashFiles('**/go.sum') }}
        restore-keys: |
          ${{ runner.os }}-go-

    - name: Download dependencies
      run: go mod download

    - name: Run unit tests
      run: make test-unit

    - name: Run integration tests
      run: make test-integration

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.out
```

### Makefile for Testing

```makefile
# Makefile for testing
.PHONY: test test-unit test-integration test-e2e clean-test

# Run all tests
test: test-unit test-integration

# Unit tests
test-unit:
    @echo "Running unit tests..."
    go test ./controllers/... -v -coverprofile=coverage-unit.out

# Integration tests
test-integration:
    @echo "Running integration tests..."
    go test ./controllers/... -tags=integration -v -coverprofile=coverage-integration.out

# End-to-end tests
test-e2e:
    @echo "Running e2e tests..."
    go test ./e2e/... -v -timeout=30m

# Generate test coverage report
test-coverage:
    @echo "Generating test coverage report..."
    gocovmerge coverage-unit.out coverage-integration.out > coverage.out
    go tool cover -html=coverage.out -o coverage.html
    go tool cover -func=coverage.out

# Clean test artifacts
clean-test:
    rm -f coverage*.out coverage.html

# Lint code
lint:
    golangci-lint run

# Format code
fmt:
    go fmt ./...
    goimports -w .

# Security scan
security:
    gosec ./...

# Run all checks
check: fmt lint security test
```

## Summary

In this chapter, we've covered:

- **Unit Testing**: Controller tests with fake clients and Ginkgo/Gomega
- **Integration Testing**: envtest framework for testing against real API server
- **End-to-End Testing**: Full application lifecycle testing
- **Test Utilities**: Fixtures, helpers, and mock clients
- **CI/CD Integration**: GitHub Actions and automated testing pipelines

## Key Takeaways

1. **Unit Tests**: Test individual components with fake clients and mocks
2. **Integration Tests**: Use envtest for testing against real Kubernetes API
3. **E2E Tests**: Validate complete application behavior in real clusters
4. **Test Helpers**: Create reusable test fixtures and utilities
5. **CI/CD**: Automate testing in development pipelines
6. **Coverage**: Track test coverage and identify untested code paths

Next, we'll explore **observability & debugging** - metrics, logging, tracing, and troubleshooting operators.

---

**Ready for the next chapter?** [Chapter 7: Observability & Debugging](07-observability.md)

*Generated for [Awesome Code Docs](https://github.com/johnxie/awesome-code-docs)*