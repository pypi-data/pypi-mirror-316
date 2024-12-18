# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from sllm_store.proto import storage_pb2 as sllm__store_dot_proto_dot_storage__pb2


class StorageStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.LoadModelAsync = channel.unary_unary(
                '/storage.Storage/LoadModelAsync',
                request_serializer=sllm__store_dot_proto_dot_storage__pb2.LoadModelRequest.SerializeToString,
                response_deserializer=sllm__store_dot_proto_dot_storage__pb2.LoadModelResponse.FromString,
                )
        self.ConfirmModel = channel.unary_unary(
                '/storage.Storage/ConfirmModel',
                request_serializer=sllm__store_dot_proto_dot_storage__pb2.ConfirmModelRequest.SerializeToString,
                response_deserializer=sllm__store_dot_proto_dot_storage__pb2.ConfirmModelResponse.FromString,
                )
        self.UnloadModel = channel.unary_unary(
                '/storage.Storage/UnloadModel',
                request_serializer=sllm__store_dot_proto_dot_storage__pb2.UnloadModelRequest.SerializeToString,
                response_deserializer=sllm__store_dot_proto_dot_storage__pb2.UnloadModelResponse.FromString,
                )
        self.ClearMem = channel.unary_unary(
                '/storage.Storage/ClearMem',
                request_serializer=sllm__store_dot_proto_dot_storage__pb2.ClearMemRequest.SerializeToString,
                response_deserializer=sllm__store_dot_proto_dot_storage__pb2.ClearMemResponse.FromString,
                )
        self.RegisterModel = channel.unary_unary(
                '/storage.Storage/RegisterModel',
                request_serializer=sllm__store_dot_proto_dot_storage__pb2.RegisterModelRequest.SerializeToString,
                response_deserializer=sllm__store_dot_proto_dot_storage__pb2.RegisterModelResponse.FromString,
                )
        self.GetServerConfig = channel.unary_unary(
                '/storage.Storage/GetServerConfig',
                request_serializer=sllm__store_dot_proto_dot_storage__pb2.GetServerConfigRequest.SerializeToString,
                response_deserializer=sllm__store_dot_proto_dot_storage__pb2.GetServerConfigResponse.FromString,
                )


class StorageServicer(object):
    """Missing associated documentation comment in .proto file."""

    def LoadModelAsync(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ConfirmModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UnloadModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ClearMem(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def RegisterModel(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetServerConfig(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StorageServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'LoadModelAsync': grpc.unary_unary_rpc_method_handler(
                    servicer.LoadModelAsync,
                    request_deserializer=sllm__store_dot_proto_dot_storage__pb2.LoadModelRequest.FromString,
                    response_serializer=sllm__store_dot_proto_dot_storage__pb2.LoadModelResponse.SerializeToString,
            ),
            'ConfirmModel': grpc.unary_unary_rpc_method_handler(
                    servicer.ConfirmModel,
                    request_deserializer=sllm__store_dot_proto_dot_storage__pb2.ConfirmModelRequest.FromString,
                    response_serializer=sllm__store_dot_proto_dot_storage__pb2.ConfirmModelResponse.SerializeToString,
            ),
            'UnloadModel': grpc.unary_unary_rpc_method_handler(
                    servicer.UnloadModel,
                    request_deserializer=sllm__store_dot_proto_dot_storage__pb2.UnloadModelRequest.FromString,
                    response_serializer=sllm__store_dot_proto_dot_storage__pb2.UnloadModelResponse.SerializeToString,
            ),
            'ClearMem': grpc.unary_unary_rpc_method_handler(
                    servicer.ClearMem,
                    request_deserializer=sllm__store_dot_proto_dot_storage__pb2.ClearMemRequest.FromString,
                    response_serializer=sllm__store_dot_proto_dot_storage__pb2.ClearMemResponse.SerializeToString,
            ),
            'RegisterModel': grpc.unary_unary_rpc_method_handler(
                    servicer.RegisterModel,
                    request_deserializer=sllm__store_dot_proto_dot_storage__pb2.RegisterModelRequest.FromString,
                    response_serializer=sllm__store_dot_proto_dot_storage__pb2.RegisterModelResponse.SerializeToString,
            ),
            'GetServerConfig': grpc.unary_unary_rpc_method_handler(
                    servicer.GetServerConfig,
                    request_deserializer=sllm__store_dot_proto_dot_storage__pb2.GetServerConfigRequest.FromString,
                    response_serializer=sllm__store_dot_proto_dot_storage__pb2.GetServerConfigResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'storage.Storage', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Storage(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def LoadModelAsync(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/LoadModelAsync',
            sllm__store_dot_proto_dot_storage__pb2.LoadModelRequest.SerializeToString,
            sllm__store_dot_proto_dot_storage__pb2.LoadModelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ConfirmModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/ConfirmModel',
            sllm__store_dot_proto_dot_storage__pb2.ConfirmModelRequest.SerializeToString,
            sllm__store_dot_proto_dot_storage__pb2.ConfirmModelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def UnloadModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/UnloadModel',
            sllm__store_dot_proto_dot_storage__pb2.UnloadModelRequest.SerializeToString,
            sllm__store_dot_proto_dot_storage__pb2.UnloadModelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def ClearMem(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/ClearMem',
            sllm__store_dot_proto_dot_storage__pb2.ClearMemRequest.SerializeToString,
            sllm__store_dot_proto_dot_storage__pb2.ClearMemResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def RegisterModel(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/RegisterModel',
            sllm__store_dot_proto_dot_storage__pb2.RegisterModelRequest.SerializeToString,
            sllm__store_dot_proto_dot_storage__pb2.RegisterModelResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetServerConfig(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.Storage/GetServerConfig',
            sllm__store_dot_proto_dot_storage__pb2.GetServerConfigRequest.SerializeToString,
            sllm__store_dot_proto_dot_storage__pb2.GetServerConfigResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
