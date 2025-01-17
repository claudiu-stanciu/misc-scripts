import $exec.resources.Akka, Akka._
import $exec.resources.Aws
import $exec.resources.Dynamo, Dynamo._
import $exec.resources.Elasticsearch, Elasticsearch._
import $exec.resources.Json
import $exec.resources.Mongo
import $exec.resources.Testing
import $exec.resources.Time
import $exec.resources.TypesafeConfig

import $exec.resources.Slick, Slick._

import $ivy.`org.scalaz::scalaz-core:7.2.12`

import scala.collection.JavaConverters._
import scala.concurrent.{Await, ExecutionContext, Future}
import scala.concurrent.duration._

import ammonite.ops._
import com.typesafe.config.ConfigFactory

import ExecutionContext.Implicits.global

repl.prompt() = "> "
interp.colors().prompt() = fansi.Color.Green
