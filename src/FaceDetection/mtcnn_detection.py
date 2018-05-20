#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood,wy
   @time: 18-5-18 下午5:47
"""
import os

import tensorflow as tf
import numpy as np
from .BaseDetection import BaseDetection
from six import iteritems, string_types



class MtcnnDetetion(BaseDetection):
    def __init__(self, config):
        super().__init__(config)
        # Todo 参数意义
        self.threshold = [
            0.6,
            0.7,
            0.7]
        self.factor = 0.709
        self.scale_factor = 1
        self.self.model_path = 'Model'

    def load(self):
        """

        :return:
        """

        with tf.Graph().as_default():
            print("Loading MTCNN Face detection model")
            self.sess = tf.Session()
            if not self.self.model_path:
                self.self.model_path, _ = os.path.split(
                    os.path.realpath(__file__))

            with tf.variable_scope('pnet'):
                data = tf.placeholder(
                    tf.float32, (None, None, None, 3), 'input')
                pnet = PNet({'data': data})
                pnet.load(os.path.join(self.model_path, 'det1.npy'), self.sess)
            with tf.variable_scope('rnet'):
                data = tf.placeholder(tf.float32, (None, 24, 24, 3), 'input')
                rnet = RNet({'data': data})
                rnet.load(os.path.join(self.model_path, 'det2.npy'), self.sess)
            with tf.variable_scope('onet'):
                data = tf.placeholder(tf.float32, (None, 48, 48, 3), 'input')
                onet = ONet({'data': data})
                onet.load(os.path.join(self.model_path, 'det3.npy'), self.sess)

            self.pnet = lambda img: self.sess.run(
                ('pnet/conv4-2/BiasAdd:0', 'pnet/prob1:0'), feed_dict={'pnet/input:0': img})
            self.rnet = lambda img: self.sess.run(
                ('rnet/conv5-2/conv5-2:0', 'rnet/prob1:0'), feed_dict={'rnet/input:0': img})
            self.onet = lambda img: self.sess.run(
                ('onet/conv6-2/conv6-2:0',
                 'onet/conv6-3/conv6-3:0',
                 'onet/prob1:0'),
                feed_dict={
                    'onet/input:0': img})
            print("MTCNN Model loaded")

        def detect(self, image):
            '''
            人脸检测接口
            :param images:
            :return: 返回照片中人脸的位置 ,以及特征点
            '''

            rects, landmarks = self.detect_face(
                image, 80)  # min face size is set to 80x80
            locations = []
            for (i, rect) in enumerate(rects):
                xmin = rect[0]
                ymax = rect[1]
                xmax = rect[0] + rect[2]
                ymin = rect[1] + rect[3]
                locations.append([ymin, xmin, ymax, xmax])

            return locations, landmarks

        def detect_face(self, img, minsize):
            # im: input image
            # minsize: minimum of faces' size
            if self.scale_factor > 1:
                img = cv2.resize(img,
                                 (int(len(img[0]) / self.scale_factor),
                                  int(len(img) / self.scale_factor)))
            factor_count = 0
            total_boxes = np.empty((0, 9))
            points = []
            h = img.shape[0]
            w = img.shape[1]
            minl = np.amin([h, w])
            m = 12.0 / minsize
            minl = minl * m
            # creat scale pyramid
            scales = []
            while minl >= 12:
                scales += [m * np.power(self.factor, factor_count)]
                minl = minl * self.factor
                factor_count += 1

            # first stage
            for j in range(len(scales)):
                scale = scales[j]
                hs = int(np.ceil(h * scale))
                ws = int(np.ceil(w * scale))
                im_data = imresample(img, (hs, ws))
                im_data = (im_data - 127.5) * 0.0078125
                img_x = np.expand_dims(im_data, 0)
                img_y = np.transpose(img_x, (0, 2, 1, 3))
                out = self.pnet(img_y)
                out0 = np.transpose(out[0], (0, 2, 1, 3))
                out1 = np.transpose(out[1], (0, 2, 1, 3))

                boxes, _ = generateBoundingBox(out1[0, :, :, 1].copy(
                ), out0[0, :, :, :].copy(), scale, self.threshold[0])

                # inter-scale nms
                pick = nms(boxes.copy(), 0.5, 'Union')
                if boxes.size > 0 and pick.size > 0:
                    boxes = boxes[pick, :]
                    total_boxes = np.append(total_boxes, boxes, axis=0)

            numbox = total_boxes.shape[0]
            if numbox > 0:
                pick = nms(total_boxes.copy(), 0.7, 'Union')
                total_boxes = total_boxes[pick, :]
                regw = total_boxes[:, 2] - total_boxes[:, 0]
                regh = total_boxes[:, 3] - total_boxes[:, 1]
                qq1 = total_boxes[:, 0] + total_boxes[:, 5] * regw
                qq2 = total_boxes[:, 1] + total_boxes[:, 6] * regh
                qq3 = total_boxes[:, 2] + total_boxes[:, 7] * regw
                qq4 = total_boxes[:, 3] + total_boxes[:, 8] * regh
                total_boxes = np.transpose(
                    np.vstack([qq1, qq2, qq3, qq4, total_boxes[:, 4]]))
                total_boxes = rerec(total_boxes.copy())
                total_boxes[:, 0:4] = np.fix(total_boxes[:, 0:4]).astype(np.int32)
                dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph = pad(
                    total_boxes.copy(), w, h)

            numbox = total_boxes.shape[0]
            if numbox > 0:
                # second stage
                tempimg = np.zeros((24, 24, 3, numbox))
                for k in range(0, numbox):
                    tmp = np.zeros((int(tmph[k]), int(tmpw[k]), 3))
                    tmp[dy[k] - 1:edy[k], dx[k] - 1:edx[k],
                    :] = img[y[k] - 1:ey[k], x[k] - 1:ex[k], :]
                    if tmp.shape[0] > 0 and tmp.shape[1] > 0 or tmp.shape[0] == 0 and tmp.shape[1] == 0:
                        tempimg[:, :, :, k] = imresample(tmp, (24, 24))
                    else:
                        return np.empty()
                tempimg = (tempimg - 127.5) * 0.0078125
                tempimg1 = np.transpose(tempimg, (3, 1, 0, 2))
                out = self.rnet(tempimg1)
                out0 = np.transpose(out[0])
                out1 = np.transpose(out[1])
                score = out1[1, :]
                ipass = np.where(score > self.threshold[1])
                total_boxes = np.hstack(
                    [total_boxes[ipass[0], 0:4].copy(), np.expand_dims(score[ipass].copy(), 1)])
                mv = out0[:, ipass[0]]
                if total_boxes.shape[0] > 0:
                    pick = nms(total_boxes, 0.7, 'Union')
                    total_boxes = total_boxes[pick, :]
                    total_boxes = bbreg(total_boxes.copy(),
                                        np.transpose(mv[:, pick]))
                    total_boxes = rerec(total_boxes.copy())

            numbox = total_boxes.shape[0]
            if numbox > 0:
                # third stage
                total_boxes = np.fix(total_boxes).astype(np.int32)
                dy, edy, dx, edx, y, ey, x, ex, tmpw, tmph = pad(
                    total_boxes.copy(), w, h)
                tempimg = np.zeros((48, 48, 3, numbox))
                for k in range(0, numbox):
                    tmp = np.zeros((int(tmph[k]), int(tmpw[k]), 3))
                    tmp[dy[k] - 1:edy[k], dx[k] - 1:edx[k],
                    :] = img[y[k] - 1:ey[k], x[k] - 1:ex[k], :]
                    if tmp.shape[0] > 0 and tmp.shape[1] > 0 or tmp.shape[0] == 0 and tmp.shape[1] == 0:
                        tempimg[:, :, :, k] = imresample(tmp, (48, 48))
                    else:
                        return np.empty()
                tempimg = (tempimg - 127.5) * 0.0078125
                tempimg1 = np.transpose(tempimg, (3, 1, 0, 2))
                out = self.onet(tempimg1)
                out0 = np.transpose(out[0])
                out1 = np.transpose(out[1])
                out2 = np.transpose(out[2])
                score = out2[1, :]
                points = out1
                ipass = np.where(score > self.threshold[2])
                points = points[:, ipass[0]]
                total_boxes = np.hstack(
                    [total_boxes[ipass[0], 0:4].copy(), np.expand_dims(score[ipass].copy(), 1)])
                mv = out0[:, ipass[0]]

                w = total_boxes[:, 2] - total_boxes[:, 0] + 1
                h = total_boxes[:, 3] - total_boxes[:, 1] + 1
                points[0:5, :] = np.tile(
                    w, (5, 1)) * points[0:5, :] + np.tile(total_boxes[:, 0], (5, 1)) - 1
                points[5:10, :] = np.tile(
                    h, (5, 1)) * points[5:10, :] + np.tile(total_boxes[:, 1], (5, 1)) - 1
                if total_boxes.shape[0] > 0:
                    total_boxes = bbreg(total_boxes.copy(), np.transpose(mv))
                    pick = nms(total_boxes.copy(), 0.7, 'Min')
                    total_boxes = total_boxes[pick, :]
                    points = points[:, pick]
            # points is stored in a very weird datastructure, this transpose it to
            # process eaiser
            simple_points = np.transpose(points)
            rects = [(max(0, (int(rect[0]))) *
                      self.scale_factor, max(0, int(rect[1])) *
                      self.scale_factor, int(rect[2] -
                                             rect[0]) *
                      self.scale_factor, int(rect[3] -
                                             rect[1]) *
                      self.scale_factor) for rect in total_boxes]
            return rects, simple_points * self.scale_factor


def layer(op):
    '''Decorator for composable network layers.'''

    def layer_decorated(self, *args, **kwargs):
        # Automatically set a name if not provided.
        name = kwargs.setdefault('name', self.get_unique_name(op.__name__))
        # Figure out the layer inputs.
        if len(self.terminals) == 0:
            raise RuntimeError('No input variables found for layer %s.' % name)
        elif len(self.terminals) == 1:
            layer_input = self.terminals[0]
        else:
            layer_input = list(self.terminals)
        # Perform the operation and get the output.
        layer_output = op(self, layer_input, *args, **kwargs)
        # Add to layer LUT.
        self.layers[name] = layer_output
        # This output is now the input for the next layer.
        self.feed(layer_output)
        # Return self for chained calls.
        return self

    return layer_decorated


class Network(object):

    def __init__(self, inputs, trainable=True):
        # The input nodes for this network
        self.inputs = inputs
        # The current list of terminal nodes
        self.terminals = []
        # Mapping from layer names to layers
        self.layers = dict(inputs)
        # If true, the resulting variables are set as trainable
        self.trainable = trainable

        self.setup()

    def setup(self):
        '''Construct the network. '''
        raise NotImplementedError('Must be implemented by the subclass.')

    def load(self, data_path, session, ignore_missing=False):
        '''Load network weights.
        data_path: The path to the numpy-serialized network weights
        session: The current TensorFlow session
        ignore_missing: If true, serialized weights for missing layers are ignored.
        '''
        data_dict = np.load(
            data_path,
            encoding='latin1').item()  # pylint: disable=no-member

        for op_name in data_dict:
            with tf.variable_scope(op_name, reuse=True):
                for param_name, data in iteritems(data_dict[op_name]):
                    try:
                        var = tf.get_variable(param_name)
                        session.run(var.assign(data))
                    except ValueError:
                        if not ignore_missing:
                            raise

    def feed(self, *args):
        '''Set the input(s) for the next operation by replacing the terminal nodes.
        The arguments can be either layer names or the actual layers.
        '''
        assert len(args) != 0
        self.terminals = []
        for fed_layer in args:
            if isinstance(fed_layer, string_types):
                try:
                    fed_layer = self.layers[fed_layer]
                except KeyError:
                    raise KeyError('Unknown layer name fed: %s' % fed_layer)
            self.terminals.append(fed_layer)
        return self

    def get_output(self):
        '''Returns the current network output.'''
        return self.terminals[-1]

    def get_unique_name(self, prefix):
        '''Returns an index-suffixed unique name for the given prefix.
        This is used for auto-generating layer names based on the type-prefix.
        '''
        ident = sum(t.startswith(prefix) for t, _ in self.layers.items()) + 1
        return '%s_%d' % (prefix, ident)

    def make_var(self, name, shape):
        '''Creates a new TensorFlow variable.'''
        return tf.get_variable(name, shape, trainable=self.trainable)

    def validate_padding(self, padding):
        '''Verifies that the padding is one of the supported ones.'''
        assert padding in ('SAME', 'VALID')

    @layer
    def conv(self,
             inp,
             k_h,
             k_w,
             c_o,
             s_h,
             s_w,
             name,
             relu=True,
             padding='SAME',
             group=1,
             biased=True):
        # Verify that the padding is acceptable
        self.validate_padding(padding)
        # Get the number of channels in the input
        c_i = int(inp.get_shape()[-1])
        # Verify that the grouping parameter is valid
        assert c_i % group == 0
        assert c_o % group == 0
        # Convolution for a given input and kernel

        def convolve(i, k): return tf.nn.conv2d(
            i, k, [1, s_h, s_w, 1], padding=padding)
        with tf.variable_scope(name) as scope:
            kernel = self.make_var(
                'weights', shape=[
                    k_h, k_w, c_i // group, c_o])
            # This is the common-case. Convolve the input without any further
            # complications.
            output = convolve(inp, kernel)
            # Add the biases
            if biased:
                biases = self.make_var('biases', [c_o])
                output = tf.nn.bias_add(output, biases)
            if relu:
                # ReLU non-linearity
                output = tf.nn.relu(output, name=scope.name)
            return output

    @layer
    def prelu(self, inp, name):
        with tf.variable_scope(name):
            i = int(inp.get_shape()[-1])
            alpha = self.make_var('alpha', shape=(i,))
            output = tf.nn.relu(inp) + tf.multiply(alpha, -tf.nn.relu(-inp))
        return output

    @layer
    def max_pool(self, inp, k_h, k_w, s_h, s_w, name, padding='SAME'):
        self.validate_padding(padding)
        return tf.nn.max_pool(inp,
                              ksize=[1, k_h, k_w, 1],
                              strides=[1, s_h, s_w, 1],
                              padding=padding,
                              name=name)

    @layer
    def fc(self, inp, num_out, name, relu=True):
        with tf.variable_scope(name):
            input_shape = inp.get_shape()
            if input_shape.ndims == 4:
                # The input is spatial. Vectorize it first.
                dim = 1
                for d in input_shape[1:].as_list():
                    dim *= int(d)
                feed_in = tf.reshape(inp, [-1, dim])
            else:
                feed_in, dim = (inp, input_shape[-1].value)
            weights = self.make_var('weights', shape=[dim, num_out])
            biases = self.make_var('biases', [num_out])
            op = tf.nn.relu_layer if relu else tf.nn.xw_plus_b
            fc = op(feed_in, weights, biases, name=name)
            return fc

    """
    Multi dimensional softmax,
    refer to https://github.com/tensorflow/tensorflow/issues/210
    compute softmax along the dimension of target
    the native softmax only supports batch_size x dimension
    """

    @layer
    def softmax(self, target, axis, name=None):
        max_axis = tf.reduce_max(target, axis, keep_dims=True)
        target_exp = tf.exp(target - max_axis)
        normalize = tf.reduce_sum(target_exp, axis, keep_dims=True)
        softmax = tf.div(target_exp, normalize, name)
        return softmax


class PNet(Network):
    def setup(self):
        (self.feed('data')  # pylint: disable=no-value-for-parameter, no-member
         .conv(3, 3, 10, 1, 1, padding='VALID', relu=False, name='conv1')
         .prelu(name='PReLU1')
         .max_pool(2, 2, 2, 2, name='pool1')
         .conv(3, 3, 16, 1, 1, padding='VALID', relu=False, name='conv2')
         .prelu(name='PReLU2')
         .conv(3, 3, 32, 1, 1, padding='VALID', relu=False, name='conv3')
         .prelu(name='PReLU3')
         .conv(1, 1, 2, 1, 1, relu=False, name='conv4-1')
         .softmax(3, name='prob1'))

        (self.feed('PReLU3')  # pylint: disable=no-value-for-parameter
         .conv(1, 1, 4, 1, 1, relu=False, name='conv4-2'))


class RNet(Network):
    def setup(self):
        (self.feed('data')  # pylint: disable=no-value-for-parameter, no-member
         .conv(3, 3, 28, 1, 1, padding='VALID', relu=False, name='conv1')
         .prelu(name='prelu1')
         .max_pool(3, 3, 2, 2, name='pool1')
         .conv(3, 3, 48, 1, 1, padding='VALID', relu=False, name='conv2')
         .prelu(name='prelu2')
         .max_pool(3, 3, 2, 2, padding='VALID', name='pool2')
         .conv(2, 2, 64, 1, 1, padding='VALID', relu=False, name='conv3')
         .prelu(name='prelu3')
         .fc(128, relu=False, name='conv4')
         .prelu(name='prelu4')
         .fc(2, relu=False, name='conv5-1')
         .softmax(1, name='prob1'))

        (self.feed('prelu4')  # pylint: disable=no-value-for-parameter
         .fc(4, relu=False, name='conv5-2'))


class ONet(Network):
    def setup(self):
        (self.feed('data')  # pylint: disable=no-value-for-parameter, no-member
         .conv(3, 3, 32, 1, 1, padding='VALID', relu=False, name='conv1')
         .prelu(name='prelu1')
         .max_pool(3, 3, 2, 2, name='pool1')
         .conv(3, 3, 64, 1, 1, padding='VALID', relu=False, name='conv2')
         .prelu(name='prelu2')
         .max_pool(3, 3, 2, 2, padding='VALID', name='pool2')
         .conv(3, 3, 64, 1, 1, padding='VALID', relu=False, name='conv3')
         .prelu(name='prelu3')
         .max_pool(2, 2, 2, 2, name='pool3')
         .conv(2, 2, 128, 1, 1, padding='VALID', relu=False, name='conv4')
         .prelu(name='prelu4')
         .fc(256, relu=False, name='conv5')
         .prelu(name='prelu5')
         .fc(2, relu=False, name='conv6-1')
         .softmax(1, name='prob1'))

        (self.feed('prelu5')  # pylint: disable=no-value-for-parameter
         .fc(4, relu=False, name='conv6-2'))

        (self.feed('prelu5')  # pylint: disable=no-value-for-parameter
         .fc(10, relu=False, name='conv6-3'))
